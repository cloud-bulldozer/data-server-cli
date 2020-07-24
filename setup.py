#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='snappy',
    version = '0.0.1',
    author='Matthew F Leader',
    author_email='mleader@redhat.com',
    description='client and command line interface to a snappy data server',
    long_description = long_description,
    download_url='https://github.com/mfleader/snappy-client',
    package=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'snappy=snappycli.main:main'
        ]
    },
    zip_safe=False,
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
    ],
    python_requires = '>=3.6'
)


