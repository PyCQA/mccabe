McCabe complexity checker
=========================

Ned's script to check McCabe complexity.

This module provides a plugin for ``flint``, the Python code checker.


Installation
------------

You can install, upgrade, uninstall ``flint-mccabe`` with these commands::

  $ pip install flint-mccabe
  $ pip install --upgrade flint-mccabe
  $ pip uninstall flint-mccabe


Standalone script
-----------------

The complexity checker can be used directly::

  $ python -m flint_mccabe --min 5 flint_mccabe.py
  ("185:1: 'PathGraphingAstVisitor.visitIf'", 5)
  ("71:1: 'PathGraph.to_dot'", 5)
  ("245:1: 'McCabeChecker.run'", 5)
  ("283:1: 'main'", 7)
  ("203:1: 'PathGraphingAstVisitor.visitTryExcept'", 5)
  ("257:1: 'get_code_complexity'", 5)


Plugin for Flint
----------------

When both ``flint`` and ``flint-mccabe`` are installed, the plugin is
available in ``flint``::

  $ flint --version
  0.1 (pep8: 1.4.2, pyflakes: 0.6.1, mccabe: 0.1)

By default the plugin is disabled.  Use the ``--max-complexity`` switch to
enable it.  It will emit a warning if the McCabe complexity of a function is
higher that the value::

    $ flint --max-complexity 10 coolproject
    ...
    coolproject/mod.py:1204:1: C901 'CoolFactory.prepare' is too complex (14)

This feature is quite useful to detect over-complex code. According to McCabe,
anything that goes beyond 10 is too complex.


Links
-----

* Cyclomatic complexity: http://en.wikipedia.org/wiki/Cyclomatic_complexity.

* Ned Batchelder's script:
  http://nedbatchelder.com/blog/200803/python_code_complexity_microtool.html


Changes
-------

0.1 - 2013-02-xx
````````````````
* First release
