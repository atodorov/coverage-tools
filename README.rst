Coverage Tools
--------------

This package is a collection of command line tools for
`coverage <http://pypi.python.org/pypi/coverage>`_ to produce verbose reports
and/or stats measurements of your test coverage.

Available tools include:

* **coverage-annotate** - prints the source code and prefixes each line with + or -
  depending on wheather it was executed during testing or not;
* **coverage-diff** - compares the annotated sources from two coverage data files to
  highlight the difference in test coverage between them;


Installation
============

Use pip to install from PyPI:

::

        pip install coverage-tools

Changelog
=========

Version 0.0.3

* New options for **coverage-annotate**
  * -N - show line numbers

Version 0.0.2

* First release on PyPI

Contributing
============

Source code and issue tracker are at https://github.com/atodorov/coverage-tools
