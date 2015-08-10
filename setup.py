#!/usr/bin/env python

import os
import sys
import unittest
from setuptools import setup, find_packages, Command

class TestRunner(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tests = unittest.defaultTestLoader.discover('.')
        runner = unittest.runner.TextTestRunner()
        result = runner.run(tests)
        sys.exit(not result.wasSuccessful())


with open('README.rst') as file:
    long_description = file.read()

config = {
    'name' : 'coverage-tools',
    'version' : '0.0.3',
    'packages' : find_packages(),
    'scripts' : [
        'coverage-annotate',
        'coverage-combine',
        'coverage-diff',
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
    'cmdclass': {'test': TestRunner},
}

setup(**config)
