
.. currentmodule:: docrep

A Python Module for intelligent reuse of docstrings
***************************************************

.. although this is a circular reference, we include the index here to make singlehtml working


.. toctree::
    :maxdepth: 1

    index

.. warning::

    Several methods have been deprecated in version 0.3. See :ref:`migrate-to-0.3`
    for details!

.. only:: html and not epub

    .. list-table::
        :stub-columns: 1
        :widths: 10 90

        * - docs
          - |docs|
        * - tests
          - |travis| |coveralls|
        * - package
          - |version| |conda| |supported-versions| |supported-implementations|

    .. |docs| image:: http://readthedocs.org/projects/docrep/badge/?version=latest
        :alt: Documentation Status
        :target: http://docrep.readthedocs.io/en/latest/?badge=latest

    .. |travis| image:: https://travis-ci.org/Chilipp/docrep.svg?branch=master
        :alt: Travis
        :target: https://travis-ci.org/Chilipp/docrep

    .. |coveralls| image:: https://coveralls.io/repos/github/Chilipp/docrep/badge.svg?branch=master
        :alt: Coverage
        :target: https://coveralls.io/github/Chilipp/docrep?branch=master

    .. |version| image:: https://img.shields.io/pypi/v/docrep.svg?style=flat
        :alt: PyPI Package latest release
        :target: https://pypi.python.org/pypi/docrep

    .. |conda| image:: https://anaconda.org/conda-forge/docrep/badges/installer/conda.svg
        :alt: conda
        :target: https://anaconda.org/conda-forge/docrep

    .. |supported-versions| image:: https://img.shields.io/pypi/pyversions/docrep.svg?style=flat
        :alt: Supported versions
        :target: https://pypi.python.org/pypi/docrep

    .. |supported-implementations| image:: https://img.shields.io/pypi/implementation/docrep.svg?style=flat
        :alt: Supported implementations
        :target: https://pypi.python.org/pypi/docrep


What's this?
============
Welcome to the **doc**\ umentation **rep**\ etition module **docrep**! This
module targets developers that develop complex and nested Python APIs and
helps them to create a well-documented piece of software.

The motivation is simple, it comes from the don’t repeat yourself principle and
tries to reuse already existing documentation code.

Suppose you have a well-documented function

.. ipython::

    In [1]: def do_something(a, b):
       ...:     """
       ...:     Add two numbers
       ...:
       ...:     Parameters
       ...:     ----------
       ...:     a: int
       ...:         The first number
       ...:     b: int
       ...:         The second number
       ...:
       ...:     Returns
       ...:     -------
       ...:     int
       ...:         `a` + `b`"""
       ...:     return a + b

and you have another function that builds upon this function

.. ipython::

    In [2]: def do_more(a, b):
       ...:     """
       ...:     Add two numbers and multiply it by 2
       ...:
       ...:     Parameters
       ...:     ----------
       ...:     a: int
       ...:         The first number
       ...:     b: int
       ...:         The second number
       ...:
       ...:     Returns
       ...:     -------
       ...:     int
       ...:         (`a` + `b`) * 2"""
       ...:     return do_something(a, b) * 2

Here for ``do_more`` we use the function ``do_something`` and actually we do
not even care about ``a`` anymore. So we could even say

.. ipython::
    :verbatim:

    In [3]: def do_more(*args, **kwargs):
       ...:     """...long docstring..."""
       ...:     return do_something(*args, **kwargs) * 2

because we only care about the result from ``do_something``. However, if we
want to change something in the parameters documentation of ``do_something``,
we would have to change it in ``do_more``. This can become a severe error
source in large and complex APIs!

So instead of copy-and-pasting the entire documentation of ``do_something``, we
want to automatically repeat the given docstrings and that's what this module
is intended for. Hence, The code above could be rewritten via

.. ipython::

    In [4]: import docrep

    In [5]: docstrings = docrep.DocstringProcessor()

    In [6]: @docstrings.get_sections(base='do_something')
       ...: @docstrings.dedent
       ...: def do_something(a, b):
       ...:     """
       ...:     Add two numbers
       ...:
       ...:     Parameters
       ...:     ----------
       ...:     a: int
       ...:         The first number
       ...:     b: int
       ...:         The second number
       ...:
       ...:     Returns
       ...:     -------
       ...:     int
       ...:         `a` + `b`"""
       ...:     return a + b

    In [7]: @docstrings.dedent
       ...: def do_more(*args, **kwargs):
       ...:     """
       ...:     Add two numbers and multiply it by 2
       ...:
       ...:     Parameters
       ...:     ----------
       ...:     %(do_something.parameters)s
       ...:
       ...:     Returns
       ...:     -------
       ...:     int
       ...:         (`a` + `b`) * 2"""
       ...:     return do_something(*args, **kwargs) * 2

    In [8]: help(do_more)

You can do the same for any other section in the objects documentation and you
can even remove or keep only specific parameters or return types (see
:meth:`~DocstringProcessor.keep_params` and
:meth:`~DocstringProcessor.delete_params`). The module intensively uses pythons
:mod:`re` module so it is very efficient. The only restriction is, that your
Python code has to be documented following the `numpy conventions`_ (i.e. it
should follow the conventions from the sphinx napoleon extension).

If your docstring does not start with an empty line as in the example above,
you have to use the :meth:`DocstringProcessor.with_indent` method. See for
example

.. ipython::

    In [9]: @docstrings.get_sections(base='do_something')
       ...: def second_example_source(a, b):
       ...:     """Summary is on the first line
       ...:
       ...:     Parameters
       ...:     ----------
       ...:     a: int
       ...:         The first number
       ...:     b: int
       ...:         The second number
       ...:
       ...:     Returns
       ...:     -------
       ...:     int
       ...:         `a` + `b`"""
       ...:     return a + b

    In [10]: @docstrings.with_indent(4)  # we indent the replacements with 4 spaces
       ....: def second_example_target(*args, **kwargs):
       ....:     """Target docstring with summary on the first line
       ....:
       ....:     Parameters
       ....:     ----------
       ....:     %(do_something.parameters)s
       ....:
       ....:     Returns
       ....:     -------
       ....:     int
       ....:         (`a` + `b`) * 2"""
       ....:     return second_example_source(*args, **kargs) * 2

    In [11]: help(second_example_target)

.. _`numpy conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


The docrep workflow
===================

The general workflow is:

1. Create an instance of the :class:`DocstringProcessor`::

       >>> from docrep import DocstringProcessor
       >>> docstrings = DocstringProcessor()

2. Analyse the docstring of a function, class or method::

       >>> @docstrings.get_sections
       ... def my_function(...):
       ...     """..."""

   Available methods for analysing the docstring are:

   .. autoclasssumm:: DocstringProcessor
       :autosummary-sections: Analysis Methods
       :autosummary-no-titles:

3. Optionally process the docstring using one of the analysis methods

   .. autoclasssumm:: DocstringProcessor
       :autosummary-sections: Extraction Methods
       :autosummary-no-titles:

4. Reuse the docstring somewhere else with one of the update methods:

   .. autoclasssumm:: DocstringProcessor
       :autosummary-sections: Updating Methods
       :autosummary-no-titles:

   For instance via::

       >>> @docstrings.dedent
       ... def my_other_function(...):
       ...     """..."""


Installation
=============
Installation simply goes via pip::

    $ pip install docrep

or via conda_::

    $ conda install -c conda-forge docrep

or from the source on github_ via::

    $ python setup.py install

.. _conda: https://conda.io/docs/
.. _github: https://github.com/Chilipp/docrep


.. note::

    When using docrep in python 2.7, there is to mention that the ``__doc__``
    attribute of classes is not writable, so something like

    .. ipython::

        @verbatim
        In [12]: @docstrings
           ....: class SomeClass(object):
           ....:     """An awesome class
           ....:
           ....:     Parameters
           ....:     ----------
           ....:     %(repeated.parameters)s
           ....:     """

    would raise an error. There are several workarounds (see
    `the issue on github <https://github.com/Chilipp/docrep/issues/5#>`__) but the
    default for python 2.7 is, to simply not modify class docstrings. You
    can, however, change this behaviour using the
    :attr:`DocstringProcessor.python2_classes` attribute.


How to add custom sections
======================

`docrep` supports the standard sections from the `numpy docstring standard`_.

You can however easily add your own section by subclassing the
:class:`DocstringProcessor` class and implement your own
:attr:`~DocstringProcessor.text_sections` and
:attr:`~DocstringProcessor.param_like_sections`.

The following example demonstrates this usage, we'll add a *Rules* that lists
some rules when to apply this method

.. ipython::

    In [13]: from docrep import DocstringProcessor

    In [13]: class RulesDocstringProcessor(DocstringProcessor):
       ....:
       ....:     param_like_sections = ["Rules"] + DocstringProcessor.param_like_sections

    In [14]: d = RulesDocstringProcessor()

    In [14]: @d.get_sections(base="increase", sections=["Parameters", "Rules"])
       ....: def increase(b):
       ....:     """Increase a number.
       ....:
       ....:     Parameters
       ....:     ----------
       ....:     b: int
       ....:         The parameters to increase
       ....:
       ....:     Rules
       ....:     -----
       ....:     greater_0
       ....:         The input parameter b must be greater than zero!
       ....:     """
       ....:     return b + 1

    In [15]: @d.with_indent(4)
       ....: def divide(a, b):
       ....:     """Divide two numbers.
       ....:
       ....:     Parameters
       ....:     ----------
       ....:     a: int
       ....:         The numerator
       ....:     b: int
       ....:         The denominator
       ....:
       ....:     Rules
       ....:     -----
       ....:     %(increase.rules)s
       ....:     """
       ....:     return a / b

    In [16]: print(divide.__doc__)

.. _numpy docstring standard: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard


API Reference
=============

.. automodule:: docrep
    :members:
    :undoc-members:
    :show-inheritance:

.. _changelog:

Changelog
*********

.. include:: ../CHANGELOG.rst

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
