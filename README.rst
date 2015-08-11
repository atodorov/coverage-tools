Coverage Tools
--------------

This package is a collection of command line tools for
`coverage <http://pypi.python.org/pypi/coverage>`_ to produce verbose reports
and/or stats measurements of your test coverage.

Available tools include:

* **coverage-annotate** - prints the source code and prefixes each line with + or -
  depending on wheather it was executed during testing or not;
* **coverage-combine** - combines several .coverage data files into one;
* **coverage-diff** - compares the annotated sources from two coverage data files to
  highlight the difference in test coverage between them;
* **coverage-report** - report on arbitrary file(s);
* **pickle2json** - convert .coverage files from pickle to JSON format; Needs
  coverage version 4.0 at least;


Installation
============

Use pip to install from PyPI:

::

        pip install coverage-tools

Changelog
=========

Version 0.0.4

* New tool **coverage-report**;
* New tool **pickle2json**;

Version 0.0.3

* New options for **coverage-annotate**

  * -N - show line numbers
  * -i - list of files to include in the report
  * -e - list of files to exclude from the report

`--include` and `--exclude` support shell globs. If none is specified all files in
the coverage data file are shown. The include list is evaluated first, then the
exclude list is evaluated.

* New options for **coverage-diff**

  * -N - show line numbers
  * -i - list of files to include in the report
  * -e - list of files to exclude from the report

The same limitations apply to all options.

* New tool **coverage-combine** which supports shell globs.

Version 0.0.2

* First release on PyPI

Contributing
============

Source code and issue tracker are at https://github.com/atodorov/coverage-tools
