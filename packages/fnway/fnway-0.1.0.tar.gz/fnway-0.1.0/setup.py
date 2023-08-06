import pathlib

import setuptools


version = (0, 1, 0)
package_name = next(pathlib.Path(__file__).parent.joinpath('src').glob('*')).name

with open('requirements.txt') as fp:
    requirements = fp.read().splitlines()

setuptools.setup(
    name=package_name,
    version='.'.join(map(str, version)),
    author='Dmitriy Ferens',
    author_email='ferensdima@gmail.com',
    description='Utilities for functional programming',
    url='https://github.com/dferens/{}'.format(package_name),
    packages=[package_name],
    package_dir={package_name: 'src/{}'.format(package_name)},
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.5',
)
