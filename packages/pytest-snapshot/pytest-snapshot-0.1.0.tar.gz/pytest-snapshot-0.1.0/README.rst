===============
pytest-snapshot
===============

.. image:: https://img.shields.io/pypi/v/pytest-snapshot.svg
    :target: https://pypi.org/project/pytest-snapshot
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-snapshot.svg
    :target: https://pypi.org/project/pytest-snapshot
    :alt: Python versions

.. image:: https://github.com/joseph-roitman/pytest-snapshot/workflows/CI/badge.svg?branch=master
   :target: https://github.com/joseph-roitman/pytest-snapshot/actions?workflow=CI
   :alt: CI Status

A plugin for snapshot testing with pytest.

This library was inspired by `jest's snapshot testing`_.
Snapshot testing can be used to test that the value of an expression does not change unexpectedly.
The added benefits of snapshot testing are that

* They are easy to create.
* They are easy to update due to changes in the expected value.

Instead of manually updating tests when the expected value of an expression changes,
the developer simply needs to

1. run ``pytest --snapshot-update`` to update the snapshot tests
2. verify that the snapshot files contain the new expected results
3. commit the snapshot changes to version control

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* snapshot testing of strings
* paths to snapshot files are controlled by the user


Requirements
------------

* Python 2.7 or 3.5+ or `PyPy`_
* `pytest`_ 3.0+


Installation
------------
You can install "pytest-snapshot" via `pip`_ from `PyPI`_::

    $ pip install pytest-snapshot


Usage
-----
A classic test could look like::

    >>> def test_function_output():
    ...     assert foo('function input') == 'expected result'

It could be re-written using snapshot testing as::

    >>> def test_function_output_with_snapshot(snapshot):
    ...     snapshot.snapshot_dir = 'snapshots/'
    ...     snapshot.assert_match(foo('function input'), 'foo_output.txt')

The author of the test should then

1. run ``pytest --snapshot-update`` to create the snapshot file ``snapshots/foo_output.txt``
   containing the output of ``foo()``.
2. verify that the content of the snapshot file is valid.
3. commit it to version control.

Now, whenever the test is run, it will assert that the output of ``foo()`` is equal to the snapshot.

What if the behaviour of ``foo()`` changes and the test starts to fail?

In the first example, the developer would need to manually update the expected result in ``test_function_output``.
This could be tedious if the expected result is very large, or there are many tests.

In the second example, the developer would need to simply

1. run ``pytest --snapshot-update``
2. verify that the snapshot file contains the new expected result
3. commit it to version control.

Snapshot testing can be used for expressions whose values are strings.
For other types, you should first create a *human readable* textual representation of the value.
For example, to snapshot test a *json-serializable* value, you could either convert it into json
or preferably convert it into the more readable yaml format using `PyYaml`_::

    >>> snapshot.assert_match(yaml.dumps(foo()), 'foo_output.yml')


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.


License
-------
Distributed under the terms of the `MIT`_ license, "pytest-snapshot" is free and open source software


Issues
------
If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/joseph-roitman/pytest-snapshot/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org
.. _`PyPy`: https://www.pypy.org/
.. _`jest's snapshot testing`: https://jestjs.io/docs/en/snapshot-testing
.. _`PyYaml`: https://pypi.org/project/PyYAML/
