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
