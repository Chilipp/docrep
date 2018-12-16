v0.2.5
======
Minor release to fix a DeprecationWarning (see https://github.com/Chilipp/docrep/issues/12)

v0.2.4
======
This new minor release has an improved documentation considering the
``keep_params`` and ``keep_types`` section and triggers new builds for python
3.7.

v0.2.3
======
This minor release contains some backward incompatible changes on how to handle
the decorators for classes in python 2.7. Thanks
`@lesteve <https://github.com/lesteve>`__ and
`@guillaumeeb <https://github.com/guillaumeeb>`__ for your input on this.

Changed
-------
* When using the decorators for classes in python 2.7, e.g. via::

      >>> @docstrings
      ... class Something(object):
      ...     "%(replacement)s"

  it does not have an effect anymore. This is because class docstrings cannot
  be modified in python 2.7 (see issue
  `#5 <https://github.com/Chilipp/docrep/issues/5#>`__). The original behaviour
  was to raise an error. You can restore the old behaviour by setting
  `DocstringProcessor.python2_classes = 'raise'`.
* Some docs have been updated (see PR
  `#7 <https://github.com/Chilipp/docrep/pull/7>`__)

Added
-----
* the `DocstringProcessor.python2_classes` to change the handling of classes
  in python 2.7

v0.2.2
======
Added
-----
* We introduce the :meth:`DocstringProcessor.get_extended_summary` and
  :meth:`DocstringProcessor.get_extended_summaryf` methods to extract the
  extended summary (see the `numpy documentation guidelines`_).
* We introduce the :meth:`DocstringProcessor.get_full_description` and
  :meth:`DocstringProcessor.get_full_descriptionf` methods to extract the
  full description (i.e. the summary plus extended summary) from a function
  docstring

.. _numpy documentation guidelines: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

v0.2.1
======
Changed
-------
* Minor bug fix in the get_sections method

v0.2.0
======
Added
-----
* Changelog
* the `get_sectionsf` and `get_sections` methods now also support non-dedented
  docstrings that start with the summary, such as::

      >>> d = DocstringProcessor()
      >>> @d.get_sectionsf('source')
      ... def source_func(a=1):
      ...     '''That's the summary
      ...
      ...        Parameters
      ...        ----------
      ...        a: int, optional
      ...            A dummy parameter description'''
      ...     pass

* the new `with_indent` and `with_indents` methods can be used to replace the
  argument in a non-dedented docstring, such as::

      >>> @d.with_indent(4)
      ... def target_func(a=1):
      ...     """Another function using arguments of source_func
      ...
      ...     Parameters
      ...     ----------
      ...     %(source.parameters)s"""
      ...     pass

      >>> print(target_func.__doc__)

      Another function using arguments of source_func

          Parameters
          ----------
          a: int, optional
              A dummy parameter description

Changed
-------
* the `get_sectionsf` and `get_sections` method now always uses the dedented
  version of the docstring. Thereby it first removes the summary.
