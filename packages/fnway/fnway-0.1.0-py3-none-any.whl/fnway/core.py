"""
Utilities for functional programming.
"""
import functools
import itertools
import operator
import queue
import random
from typing import (
    Callable, Any, List, Union, Mapping, Sequence, Tuple, TypeVar,
    Iterable, MutableSequence, MutableSet, MutableMapping, Iterator
)

from frozendict import frozendict


T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')
R = TypeVar('R')


class _fmeta(type):
    def __getattr__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return operator.attrgetter(item)


class f(metaclass=_fmeta):
    """
    Works like `functools.partial` but also:
     * allows to pass ellipsis `...` to indicate position of later arguments
     * attribute access on class returns attrgetter
    """

    def __init__(self, *args, **kwargs):
        assert args
        fn = args[0]
        args = args[1:]

        if not callable(fn):
            raise TypeError('the first argument must be callable')

        # tuple.count does not work when == returns non-bool object
        no_elipsis = sum(1 for arg in args if arg is ...)

        if no_elipsis == 0:
            self._args_before = args
            self._args_after = ()
        elif no_elipsis == 1:
            i = args.index(...)
            self._args_before = args[:i]
            self._args_after = args[i + 1:]
        else:
            raise TypeError('ellipsis can appear only once')

        self._fn = fn
        self._kwargs = frozendict(kwargs)

    def __repr__(self):
        qualname = type(self).__qualname__
        args = [repr(self._fn)]
        args.extend(repr(x) for x in self._args_before)
        args.extend('...')
        args.extend(repr(x) for x in self._args_after)
        args.extend('{}={!r}'.format(k, v) for k, v in self._kwargs.items())
        return '{}({})'.format(qualname, ', '.join(args))

    def _id(self):
        return (self._fn, self._args_before, self._args_after, self._kwargs)

    def __eq__(self, other):
        if isinstance(other, f):
            return self._id() == other._id()
        else:
            return False

    def __hash__(self):
        return hash(self._id())

    def __call__(self, *args, **kwargs):
        new_args = (self._args_before + args + self._args_after)
        return self._fn(*new_args, **self._kwargs, **kwargs)


def partialize(fn: Callable):
    """
    Allows function to become `partial` when ellipsis `...`
    is passed instead of one of it arguments.
    """

    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        if any(a is ... for a in args):
            return f(fn, *args, **kwargs)
        else:
            return fn(*args, **kwargs)

    return decorated


_NOT_SET = type('_NOT_SET', (), {})()


@partialize
def nth(coll: Sequence[T], n: int, *, default: R = _NOT_SET) -> Union[T, R]:
    index = n - 1
    if default is _NOT_SET:
        return coll[index]
    else:
        try:
            return coll[index]
        except IndexError:
            return default


@partialize
def first(coll: Sequence[T], *, default: R = _NOT_SET) -> Union[T, R]:
    return nth(coll, 1, default=default)


@partialize
def second(coll: Sequence[T], *, default: R = _NOT_SET) -> Union[T, R]:
    return nth(coll, 2, default=default)


@partialize
def last(coll: Sequence[T], *, default: R = _NOT_SET) -> Union[T, R]:
    if default is _NOT_SET:
        return coll[-1]
    else:
        try:
            return coll[-1]
        except IndexError:
            return default


@partialize
def take(coll: Iterable[T], size: int) -> Iterable[T]:
    """
    Return first `size` items from sequence.
    """
    if hasattr(coll, '__getitem__'):
        return coll[:size]
    elif hasattr(coll, '__next__'):
        return itertools.islice(coll, size)
    else:
        raise NotImplementedError


@partialize
def pipe(initial, *fns):
    """
    Applies functions sequentially to first argument, return result of last fn.

        >>> pipe(
        ...     range(5),
        ...     list,
        ...     sum,
        ...     print
        ... )
        10

    """
    # A next improvement may be to use macros to:
    #  1) transform actual calls with `...` into lambdas
    #  2) transform `foreach` into generator/list expression (for speedup)
    #  3) transform whole pipe expression into one call (for speedup)
    #     >>> pipe[
    #     >>>     matchers,
    #     >>>     foreach(sce.calc_distance(..., pattern)),
    #     >>>     list,
    #     >>>     argmin_n(..., n=2),
    #     >>>     tuple,
    #     >>> ]
    #
    #     ... tuple(
    #     ...     argmin_n(
    #     ...         list(
    #     ...             (sce.calc_distance(x, pattern) for x in matchers)
    #     ...         ),
    #     ...         n=2
    #     ...     )
    #     ... )

    prev = initial
    calls = []
    for fn in fns:
        prev = fn(prev)
        calls.append(prev)  # for debugging
    return prev


def identity(x: T) -> T:
    return x


def colgetter(d: Union[Mapping, Sequence]) -> Callable[[Any], Any]:
    """
    Return callable which accepts keys/indices and returns values from given dict/list.
    """
    return d.__getitem__


@partialize
def group_by(coll: Iterable[T], key: Callable[[Any], K] = identity) -> List[Tuple[K, List[T]]]:
    """
    Generator which groups collection by given key and yields `(k, <group>)` pairs.
    Uses `val` function to transform group.
    """
    return [
        (k, list(v_list))
        for k, v_list in itertools.groupby(sorted(coll, key=key), key=key)
    ]


@partialize
def split_by(coll: Iterable[T], predicate: Callable[[T], bool]) -> Tuple[List[T], List[T]]:
    result = ([], [])

    for item in coll:
        result[predicate(item)].append(item)

    false_list, true_list = result
    return (false_list, true_list)


@partialize
def partition(coll: List[T], size: int, *, step: int = None) -> Iterable[List[T]]:
    """
    Returns generator of lists of `size` items each.
    If `step` is not given, defaults to `size` i.e. partitions do not overlap.
    """
    return [
        coll[i: i + size]
        for i in range(0, len(coll) - size + 1, step)
    ]


def fmap(fn: Callable[[T], R]) -> Callable[[Iterable[T]], List[R]]:
    """
    Same as `f(map, fn)`.
    Map given function onto sequence or mapping passed later, returning list.
    """

    def mapper(coll: Iterable[T]) -> List[R]:
        return [fn(x) for x in coll]

    return mapper


def ffilter(fn: Callable[[T], bool]) -> Callable[[Iterable[T]], List[T]]:
    """
    Same as `f(filter, fn)`.
    """

    def wrapper(coll):
        return [x for x in coll if fn(x)]

    return wrapper


def repeat(fn: Callable[[], R]) -> Callable[[int], Iterable[R]]:
    return lambda times: (fn() for _ in range(times))


def do(*fns: Callable[[T], Any]) -> Callable[[T], Any]:
    """
    Return callable, which accepts single value, executes functions and passes value further.
    The return values of functions are ignored.
    """

    def wrapper(val):
        for fn in fns:
            fn(val)
        return val

    return wrapper


def juxt(*fns: Callable[[T], Any]) -> Callable[[T], Tuple]:
    """
    Return function, which returns tuple containing result of each function.
    """

    def wrapper(*args, **kwargs):
        return tuple(fn(*args, **kwargs) for fn in fns)

    return wrapper


def pairing(fn: Callable[[T], R]) -> Callable[[T], Tuple[T, R]]:
    """
    Function will return 2-item tuples of (argument, fn(argument).
    """
    return juxt(identity, fn)


def comp(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Compose functions.
    """

    def wrapper(x):
        return functools.reduce(
            lambda val, fn: fn(val),
            reversed(fns),
            x
        )

    return wrapper


@partialize
def apply(fn: Callable, args: Iterable, kwargs: Mapping = frozendict()):
    return fn(*args, **kwargs)


def shuffled(coll: Iterable[T]) -> List[T]:
    """
    Returns new shuffled sequence.
    """
    return pipe(coll, list, do(random.shuffle))


@partialize
def conj(coll, val, **kwargs):
    """
    Add item to the collection. If it's a sequence, adds to the end.
    If collection is mutable (list, etc.), mutates it in-place,
    returns new immutable collection otherwise.
    When adding to a dict, value must be 2-element tuple.
    """
    if isinstance(coll, MutableSequence):
        coll.append(val)
        return coll
    elif isinstance(coll, MutableSet):
        coll.add(val)
        return coll
    elif isinstance(coll, MutableMapping):
        k, v = val
        coll[k] = v
        return coll
    elif isinstance(coll, tuple):
        return coll + (val,)
    elif isinstance(coll, queue.Queue):
        coll.put(val, **kwargs)
    elif isinstance(coll, frozenset):
        return coll.union({val})
    elif isinstance(coll, frozendict):
        k, v = val
        return coll.copy(**{k: v})
    elif isinstance(coll, Iterator):
        return itertools.chain(coll, [val])
    else:
        raise NotImplementedError(type(coll))


@partialize
def concat(seq: Iterable[T], *seqs: Iterable[T]) -> Iterable[T]:
    """
    Join sequences together.
    """
    out = seq
    for s in seqs:
        for v in s:
            out = conj(out, v)
    return out


@partialize
def slurp(file: Union[str, int], *, mode='rt', **kwargs) -> Union[str, bytes]:
    """
    Read all contents from file as string/bytes object.
    """
    with open(file, mode=mode, **kwargs) as fp:
        return fp.read()


@partialize
def spit(file: Union[str, int], data: Union[str, bytes], *, mode='wt', **kwargs):
    """
    Opposite to `slurp`. Write string/bytes object to a file.
    """
    with open(file, mode=mode, **kwargs) as fp:
        fp.write(data)
