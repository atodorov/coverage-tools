#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

config = {
    'name' : 'coverage-tools',
    'version' : '0.0.1',
    'packages' : find_packages(),
    'scripts' : [
        'coverage-diff',
        'coverage-annotate',
    ],
    'author' : 'Alexander Todorov',
    'author_email' : 'atodorov@nospam.otb.bg',
    'license' : 'MIT',
    'description' : 'Additional tools for Python coverage',
    'long_description' : long_description,
    'url' : 'https://github.com/atodorov/coverage-tools',
    'keywords' : ['code', 'coverage', 'testing'],
    'classifiers' : [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing ',
    ],
    'zip_safe' : False,
    'install_requires' : ['coverage'],
    'test_suite' : '__main__.execute_tests',
}

setup(**config)
