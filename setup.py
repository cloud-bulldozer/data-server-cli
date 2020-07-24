#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools, os, io

CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()



setuptools.setup(
    name='snappycli',
    version = '0.0.1',
    author='Matthew F Leader',
    author_email='mleader@redhat.com',
    description='client and command line interface to a snappy data server',
    long_description = README,
    long_description_content_type = 'text/markdown',
    download_url='https://github.com/mfleader/snappyCLI',
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


