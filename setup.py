#!/usr/bin/env python3

from setuptools import setup

from syncipy.version import __version__

setup(
    name='syncipy',
    version=__version__,
    description='Python package to synchronize IP address with dynamic DNS services',
    author='Balazs Kocso',
    author_email='kocsob@users.noreply.github.com',
    packages=['syncipy'],
    install_requires=[
        'requests',
    ],
    extras_require={
        'dev': [
            'flake8',
            'pyfakefs',
            'pytest',
            'pytest-pep8',
            'pytest-cov',
        ]
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: Name Service (DNS)",
    ],
)
