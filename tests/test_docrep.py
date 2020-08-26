# -*- coding: utf-8 -*-
import unittest
import re
import docrep
import six
import warnings


if six.PY2:
    class _BaseTest(unittest.TestCase):
        'A test which checks if the specified warning was raised'

        def assertWarns(self, *args, **kwargs):
            "Do nothing here since it is not implemented in Python2"
            return warnings.catch_warnings(record=True)

        def assertWarnsRegex(self, *args, **kwargs):
            "Do nothing here since it is not implemented in Python2"
            return warnings.catch_warnings(record=True)

else:
    _BaseTest = unittest.TestCase


class TestSafeModulo(_BaseTest):
    """Test case for the :func:`docrep.safe_modulo` function"""

    def test_basic(self):
        """Test whether a normal string modulo operation works as it should"""
        s = "That's a %s test of with some %% symbols in it"
        self.assertEqual(docrep.safe_modulo(s, 'simple'), s % 'simple')

        s = "That's another %(simple)s test with some %% in it"
        self.assertEqual(docrep.safe_modulo(s, {'simple': 'simple'}),
                         s % {'simple': 'simple'})

    def test_missing_kwarg(self):
        """Test whether it works if we have a missing argument"""
        s = "That's a %(basic)s test of with missing %(symbols)s in it"
        ref = "That's a basic test of with missing %(symbols)s in it"
        with self.assertWarns(SyntaxWarning):
            self.assertEqual(docrep.safe_modulo(s, {'basic': 'basic'}), ref)

    def test_missing_arg(self):
        """Test whether it works if we have another % argument in it"""
        s = "That's a %(basic)s test of with additional % and %s in it"
        ref = "That's a basic test of with additional % and %s in it"
        self.assertEqual(docrep.safe_modulo(s, {'basic': 'basic'}), ref)

    def test_missing_kwarg_and_arg(self):
        """Test whether it works if we have another % argument in it"""
        s = "That's a %(basic)s test of with missing %(symbols)s and % in it"
        ref = "That's a basic test of with missing %(symbols)s and % in it"
        with self.assertWarns(SyntaxWarning):
            self.assertEqual(docrep.safe_modulo(s, {'basic': 'basic'}), ref)

    def test_incomplete_format(self):
        ref = "That's a basic test of with missing format for %(symbols)"
        with self.assertRaises(ValueError):
            docrep.safe_modulo(ref, {'symbols': 'test'})


numbered_list = """
1. some item
2. some other item
"""

description_list = """
item1
    Description of item 1
item2
    Description of item 2
"""

random_text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin sagittis, felis
ut tempus dapibus, est lorem iaculis augue, sit amet rutrum odio nulla a est.
Fusce egestas viverra molestie. Donec quis justo congue, hendrerit mi sed,
mattis quam. Donec laoreet tristique aliquam. Etiam convallis tellus id est
pretium accumsan"""


summary = "That's a summary of what the function does"

multiline_summary = "That's a multiline\nsummary of what the function does"

parameters_header = "Parameters\n----------"

other_parameters_header = "Other Parameters\n----------------"

returns_header = "Returns\n-------"

examples_header = "Examples\n--------"

notes_header = "Notes\n-----"

see_also_header = "See Also\n--------"

simple_param = """param: str
    That's the description for one parameter"""

simple_param2 = """Another_1 : with blanks
    And so on"""

simple_multiline_param = """multiline_param: str
    The docstring of
    this one spans
    multiple lines"""

complex_param = """complex: test
    A complex parameter

    1. with intermediate list
    2. and so on"""

very_complex_param = """very_complex: another type
    Where the description goes
    over multiple lines

    with some
        description lists
    in it
        and also

    a

    1. numbered list
    2. that goes
       over multiple lines"""

simple_return_type = "type1\n" + ''.join(simple_param.splitlines(True)[1:])

simple_multiline_return_type = "type2\n" + ''.join(
    simple_multiline_param.splitlines(True)[1:])

complex_return_type = "type3\n" + ''.join(complex_param.splitlines(True)[1:])

very_complex_return_type = 'complex_type3\n' + ''.join(
    very_complex_param.splitlines(True)[1:])

examples = """Just some examples::

    >>> a = 1 + 3

which continue and end::

    >>> with indentation:
    ...     to_check"""


notes = """Just some notes with

    1. an intermediate list
    2. because we can

and a final statement
over 2 lines"""


see_also = """Just some notes with

    1. an intermediate list
    2. because we can

and a final statement
over 2 lines"""


class TestDocstringProcessor(_BaseTest):
    """Test case for the :class:`docrep.DocstringProcessor` test case"""

    def setUp(self):
        self.ds = docrep.DocstringProcessor()

    def tearDown(self):
        del self.ds

    def test_get_sections(self, indented=False):
        """Test whether the parameter sections are extracted correctly"""
        if indented:
            def indent(s):
                return ' ' * 4 + ('\n' + ' ' * 4).join(s.splitlines())
        else:
            def indent(s):
                return s

        self.params_section = ps = simple_param + '\n' + complex_param
        self.other_params_section = ops = (
            simple_multiline_param + '\n' + very_complex_param)
        self.returns_section = rs = (
            simple_return_type + '\n' + very_complex_return_type)

        def test():
            pass

        test.__doc__ = (
            summary + '\n\n' + indent(
                random_text + '\n\n' +
                parameters_header + '\n' + ps + '\n\n' +
                other_parameters_header + '\n' + ops + '\n\n' +
                returns_header + '\n' + rs + '\n\n' +
                examples_header + '\n' + examples + '\n\n' +
                notes_header + '\n' + notes + '\n\n' +
                see_also_header + '\n' + see_also))
        base = 'test'

        decorator = self.ds.get_sections(
            base=base,
            sections=['Examples', 'Parameters', 'Other Parameters',
                      'Returns', 'Notes', 'See Also', 'References'])
        decorator(test)

        ds = self.ds
        self.assertEqual(ds.params[base + '.parameters'], ps)
        self.assertEqual(ds.params[base + '.other_parameters'],
                         ops)
        self.assertEqual(ds.params[base + '.returns'], rs)
        self.assertEqual(ds.params[base + '.examples'], examples)
        self.assertEqual(ds.params[base + '.notes'], notes)
        self.assertEqual(ds.params[base + '.see_also'], see_also)
        self.assertEqual(ds.params[base + '.references'], '')

    def test_get_sections_indented(self):
        self.test_get_sections(indented=True)

    def test_dedent(self):
        self.test_get_sections()

        with self.assertWarns(SyntaxWarning):
            @self.ds.dedent
            def test2():
                """
                A test function with used docstring from another

                Parameters
                ----------
                %(test.parameters)s
                %(missing)s

                Examples
                --------
                %(test.examples)s"""

        ref = ("A test function with used docstring from another\n"
               "\n"
               "Parameters\n"
               "----------\n" +
               self.params_section + '\n%(missing)s\n\n' +
               examples_header + '\n' + examples)

        self.assertEqual(test2.__doc__, ref)

    def test_with_indent(self):
        self.test_get_sections_indented()

        with self.assertWarns(SyntaxWarning):
            @self.ds.with_indent(16)
            def test2():
                """A test function with used docstring from another

                Parameters
                ----------
                %(test.parameters)s
                %(missing)s

                Examples
                --------
                %(test.examples)s"""

        ref = ("A test function with used docstring from another\n"
               "\n"
               "Parameters\n"
               "----------\n" +
               self.params_section + '\n%(missing)s\n\n' +
               examples_header + '\n' + examples)

        ref = '\n'.join(' ' * 16 + l if l.strip() and i else l
                        for i, l in enumerate(ref.splitlines()))

        s = '\n'.join(l.rstrip() for l in test2.__doc__.splitlines())
        self.assertEqual(s, ref)

    def test_dedents(self):
        self.test_get_sections()
        s = """
            A test function with used docstring from another

            Parameters
            ----------
            %(test.parameters)s
            %(missing)s

            Examples
            --------
            %(test.examples)s"""

        ref = ("A test function with used docstring from another\n"
               "\n"
               "Parameters\n"
               "----------\n" +
               self.params_section + '\n%(missing)s\n\n' +
               examples_header + '\n' + examples)

        with self.assertWarns(SyntaxWarning):
            res = self.ds.dedents(s)

        self.assertEqual(res, ref)

    def test_get_docstring(self):
        """Test the :meth:`docrep.DocstringProcessor.save_docstring` method"""
        @self.ds.get_docstring(base='test')
        def test():
            "Just a test\n\nwith something"
            pass

        self.assertEqual(self.ds.params['test'],
                         "Just a test\n\nwith something")

    def test_get_summary(self):
        """Test whether the summary is extracted correctly"""

        doc = (
            random_text + '\n\n' + parameters_header + '\n' + complex_param)

        def test_oneline():
            pass
        test_oneline.__doc__ = summary + '\n\n' + doc

        self.ds.get_summary(base='test1')(test_oneline)
        self.assertEqual(self.ds.params['test1.summary'], summary)

        def test_multiline():
            pass
        test_multiline.__doc__ = multiline_summary + '\n\n' + doc

        self.ds.get_summary(base='test2')(test_multiline)
        self.assertEqual(self.ds.params['test2.summary'], multiline_summary)

        def test_summary_only():
            pass
        test_summary_only.__doc__ = summary
        self.ds.get_summary(base='test3')(test_summary_only)
        self.assertEqual(self.ds.params['test3.summary'], summary)

    def test_get_extended_summary(self):
        """Test whether the extended summary is extracted correctly"""

        doc = (
            random_text + '\n\n' + parameters_header + '\n' + complex_param)

        def test_basic():
            pass
        test_basic.__doc__ = summary + '\n\n' + doc

        self.ds.get_extended_summary(base='test1')(test_basic)
        self.assertEqual(self.ds.params['test1.summary_ext'],
                         random_text.strip())

        def test_no_extended_summary():
            pass
        test_no_extended_summary.__doc__ = doc

        self.ds.get_extended_summary(base='test2')(test_no_extended_summary)
        self.assertEqual(self.ds.params['test2.summary_ext'], '')

        def test_no_params():
            pass
        test_no_params.__doc__ = summary + '\n\n' + random_text
        self.ds.get_extended_summary(base='test3')(test_no_params)
        self.assertEqual(self.ds.params['test3.summary_ext'],
                         random_text.strip())

    def test_get_full_description(self):
        """Test whether the full description is extracted correctly"""

        doc = (
            random_text + '\n\n' + parameters_header + '\n' + complex_param)

        def test_basic():
            pass
        test_basic.__doc__ = summary + '\n\n' + doc

        self.ds.get_full_description(base='test1')(test_basic)
        self.assertEqual(self.ds.params['test1.full_desc'],
                         summary + '\n\n' + random_text.strip())

        def test_no_extended_summary():
            pass
        test_no_extended_summary.__doc__ = doc

        self.ds.get_full_description(base='test2')(test_no_extended_summary)
        self.assertEqual(self.ds.params['test2.full_desc'],
                         random_text.strip())

        def test_no_params():
            pass
        test_no_params.__doc__ = summary + '\n\n' + random_text
        self.ds.get_full_description(base='test3')(test_no_params)
        self.assertEqual(self.ds.params['test3.full_desc'],
                         summary + '\n\n' + random_text.strip())

    # -------------------------------------------------------------------------
    # ------------------------------ Keep tests -------------------------------
    # -------------------------------------------------------------------------

    # ------------------------- Keep Parameters tests -------------------------

    def _test_keep_params(self, *pdescs):
        """Test whether it works to keep parameters"""
        all_pdescs = [simple_param, simple_param2, complex_param,
                      very_complex_param, simple_multiline_param]
        params = [pdesc.splitlines()[0].split(':')[0].strip()
                  for pdesc in pdescs]
        joined_pdescs = '\n'.join(pdescs)
        ds = docrep.DocstringProcessor()
        ds.params['selected'] = joined_pdescs
        ds.keep_params('selected', *params)
        # check single
        self.assertEqual(ds.params['selected.' + '|'.join(params)],
                         joined_pdescs,
                         msg='Wrong description for params {}'.format(params))
        # full check
        ds.params['all'] = '\n'.join(all_pdescs)
        ds.keep_params('all', *params)
        self.assertEqual(ds.params['all.' + '|'.join(params)],
                         joined_pdescs,
                         msg='Wrong description for params {}'.format(params))

    def test_keep_simple_param(self):
        """Test whether the simple param is kept"""
        self._test_keep_params(simple_param)
        self._test_keep_params(simple_param, very_complex_param)

    def test_keep_simple_param2(self):
        """Test whether the simple param is kept"""
        self._test_keep_params(simple_param2)
        self._test_keep_params(simple_param2, simple_multiline_param)

    def test_keep_multiline_simple_param(self):
        """Test whether the simple multiline param is kept"""
        self._test_keep_params(simple_multiline_param)
        self._test_keep_params(complex_param, simple_multiline_param)

    def test_keep_complex_param(self):
        """Test whether the complex param is kept"""
        self._test_keep_params(complex_param)
        self._test_keep_params(simple_param, complex_param)

    def test_keep_very_complex_param(self):
        """Test whether the very complex param is kept"""
        self._test_keep_params(very_complex_param)
        self._test_keep_params(complex_param, very_complex_param)

    # ----------------------- Keep Return types tests -------------------------

    def _test_keep_types(self, *tdescs):
        """Test whether it works to keep return types"""
        all_tdescs = [simple_return_type, complex_return_type,
                      very_complex_return_type, simple_multiline_return_type]
        types = [tdesc.splitlines()[0].strip()
                 for tdesc in tdescs]
        joined_tdescs = '\n'.join(tdescs)
        ds = docrep.DocstringProcessor()
        ds.params['selected'] = joined_tdescs
        ds.keep_types('selected', 'kept', *types)
        # check single
        self.assertEqual(ds.params['selected.kept'], joined_tdescs,
                         msg='Wrong description for return types {}'.format(
                            types))
        # full check
        ds.params['all'] = '\n'.join(all_tdescs)
        ds.keep_types('all', 'kept', *types)
        self.assertEqual(ds.params['all.kept'], joined_tdescs,
                         msg='Wrong description for return types {}'.format(
                            types))

    def test_keep_simple_type(self):
        """Test whether the simple return type is kept"""
        self._test_keep_types(simple_return_type)
        self._test_keep_types(simple_return_type, simple_multiline_return_type)

    def test_keep_multiline_simple_type(self):
        """Test whether the simple multiline return type is kept"""
        self._test_keep_types(simple_multiline_return_type)
        self._test_keep_types(complex_return_type,
                              simple_multiline_return_type)

    def test_keep_complex_type(self):
        """Test whether the complex return type is kept"""
        self._test_keep_types(complex_return_type)
        self._test_keep_types(complex_return_type, very_complex_return_type)

    def test_keep_very_complex_type(self):
        """Test whether the very complex return type is kept"""
        self._test_keep_types(very_complex_return_type)
        self._test_keep_types(simple_return_type, very_complex_return_type)

    # -------------------------------------------------------------------------
    # -------------------------- Delete tests ---------------------------------
    # -------------------------------------------------------------------------

    # ------------------------- Delete Parameters tests -----------------------

    def _test_delete_param(self, *pdescs):
        """General method  to test whether the delete_params method works"""
        all_pdescs = [simple_param, simple_param2, complex_param,
                      very_complex_param, simple_multiline_param]
        ds = docrep.DocstringProcessor()
        ds.params['all'] = ref = '\n'.join(all_pdescs)
        params = [pdesc.splitlines()[0].split(':')[0].strip()
                  for pdesc in pdescs]
        ds.delete_params('all', *params)
        for pdesc in pdescs:
            ref = re.sub('\n?' + pdesc + '\n?', '\n', ref).strip()
        self.assertEqual(ds.params['all.no_' + '|'.join(params)], ref,
                         msg='Wrong description for params {}'.format(params))

    def test_delete_simple_param(self):
        """Test whether the deletion of a simple parameter works"""
        self._test_delete_param(simple_param)
        self._test_delete_param(simple_param, complex_param)

    def test_delete_simple_param2(self):
        """Test whether the deletion of a simple parameter works"""
        self._test_delete_param(simple_param2)
        self._test_delete_param(simple_param2, very_complex_param)

    def test_delete_simple_multiline_param(self):
        """Test whether the deletion of a simple multiline parameter works"""
        self._test_delete_param(simple_multiline_param)
        self._test_delete_param(simple_param2, simple_multiline_param)

    def test_delete_complex_param(self):
        """Test whether the deletion of a complex parameter works"""
        self._test_delete_param(complex_param)
        self._test_delete_param(complex_param, simple_multiline_param)

    def test_delete_very_complex_param(self):
        """Test whether the deletion of a very complex parameter works"""
        self._test_delete_param(very_complex_param)
        self._test_delete_param(complex_param, very_complex_param)

    # ----------------------- Delete Return types tests -----------------------

    def _test_delete_types(self, *tdescs):
        """Test whether it works to keep return types"""
        all_tdescs = [simple_return_type, complex_return_type,
                      very_complex_return_type, simple_multiline_return_type]
        types = [tdesc.splitlines()[0].strip()
                 for tdesc in tdescs]
        ds = docrep.DocstringProcessor()
        # full check
        ds.params['all'] = ref = '\n'.join(all_tdescs)
        ds.delete_types('all', 'deleted', *types)
        for tdesc in tdescs:
            ref = re.sub('\n?' + tdesc + '\n?', '\n', ref).strip()
        self.assertEqual(ds.params['all.deleted'], ref,
                         msg='Wrong description for return types {}'.format(
                            types))

    def test_delete_simple_type(self):
        """Test whether the simple return type is deleted"""
        self._test_delete_types(simple_return_type)
        self._test_delete_types(simple_return_type,
                                simple_multiline_return_type)

    def test_delete_multiline_simple_type(self):
        """Test whether the simple multiline return type is deleted"""
        self._test_delete_types(simple_multiline_return_type)
        self._test_delete_types(complex_return_type,
                                simple_multiline_return_type)

    def test_delete_complex_type(self):
        """Test whether the complex return type is deleted"""
        self._test_delete_types(complex_return_type)
        self._test_delete_types(complex_return_type, very_complex_return_type)

    def test_delete_very_complex_type(self):
        """Test whether the very complex return type is deleted"""
        self._test_delete_types(very_complex_return_type)
        self._test_delete_types(simple_return_type, very_complex_return_type)

    def test_delete_kwargs(self):
        """Test whether the ``*args`` and ``**kwargs`` are deleted correctly"""
        params_section = simple_param + '\n' + complex_param
        args_desc = ("``*args``\n"
                     "    Any additional\n"
                     "    arguments passed to another function")
        kwargs_desc = ("``**kwargs``\n"
                       "    Any additional keyword\n"
                       "    arguments passed to another function")
        self.ds.params['test'] = (params_section + '\n' + args_desc + '\n' +
                                  kwargs_desc)
        self.ds.delete_kwargs('test', 'args', 'kwargs')
        self.assertEqual(self.ds.params['test.no_args_kwargs'], params_section)

        with self.assertWarns(UserWarning):
            self.ds.delete_kwargs('test')

    @unittest.skipIf(not six.PY2, "Only implemented for python 2.7")
    def test_py2_classes(self):
        """Test the handling of classes in python 2.7"""
        # this should work
        @self.ds
        class Test(object):
            """docs"""
        # this should not
        self.ds.python2_classes = 'raise'
        try:
            @self.ds
            class Test2(object):
                """docs"""
        except AttributeError:
            pass
        else:
            self.fail("Should have raised AttributeError!")


class DepreceationsTest(_BaseTest):
    """Test case for depreceated methods"""

    def setUp(self):
        self.ds = docrep.DocstringProcessor()

    def tearDown(self):
        del self.ds

    def test_get_sectionsf(self, indented=False):
        """Test whether the parameter sections are extracted correctly"""
        if indented:
            def indent(s):
                return ' ' * 4 + ('\n' + ' ' * 4).join(s.splitlines())
        else:
            def indent(s):
                return s

        self.params_section = ps = simple_param + '\n' + complex_param
        self.other_params_section = ops = (
            simple_multiline_param + '\n' + very_complex_param)
        self.returns_section = rs = (
            simple_return_type + '\n' + very_complex_return_type)

        def test():
            pass

        test.__doc__ = (
            summary + '\n\n' + indent(
                random_text + '\n\n' +
                parameters_header + '\n' + ps + '\n\n' +
                other_parameters_header + '\n' + ops + '\n\n' +
                returns_header + '\n' + rs + '\n\n' +
                examples_header + '\n' + examples + '\n\n' +
                notes_header + '\n' + notes + '\n\n' +
                see_also_header + '\n' + see_also))
        base = 'test'

        with self.assertWarnsRegex(DeprecationWarning, 'get_sectionsf'):
            decorator = self.ds.get_sectionsf(
                base, sections=['Examples', 'Parameters', 'Other Parameters',
                                'Returns', 'Notes', 'See Also', 'References'])
        decorator(test)

        ds = self.ds
        self.assertEqual(ds.params[base + '.parameters'], ps)
        self.assertEqual(ds.params[base + '.other_parameters'],
                         ops)
        self.assertEqual(ds.params[base + '.returns'], rs)
        self.assertEqual(ds.params[base + '.examples'], examples)
        self.assertEqual(ds.params[base + '.notes'], notes)
        self.assertEqual(ds.params[base + '.see_also'], see_also)
        self.assertEqual(ds.params[base + '.references'], '')

    def test_dedents(self):
        self.test_get_sectionsf()
        s = """
            A test function with used docstring from another

            Parameters
            ----------
            %(test.parameters)s
            %(missing)s

            Examples
            --------
            %(test.examples)s"""

        ref = ("A test function with used docstring from another\n"
               "\n"
               "Parameters\n"
               "----------\n" +
               self.params_section + '\n%(missing)s\n\n' +
               examples_header + '\n' + examples)

        with self.assertWarnsRegex(DeprecationWarning, 'dedents'):
            res = self.ds.dedents(s)

        self.assertEqual(res, ref)

    def test_keep_params_s(self):
        all_pdescs = [simple_param, simple_param2, complex_param,
                      very_complex_param, simple_multiline_param]
        pdescs = [simple_param, very_complex_param]
        params = [pdesc.splitlines()[0].split(':')[0].strip()
                  for pdesc in pdescs]
        joined_pdescs = '\n'.join(pdescs)
        ds = docrep.DocstringProcessor()
        with self.assertWarnsRegex(DeprecationWarning, 'keep_params_s'):
            txt = ds.keep_params_s('\n'.join(all_pdescs), params)
        # check single
        self.assertEqual(txt, joined_pdescs,
                         msg='Wrong description for params {}'.format(params))

    def test_get_summaryf(self):
        """Test whether the summary is extracted correctly"""

        doc = (
            random_text + '\n\n' + parameters_header + '\n' + complex_param)

        def test_oneline():
            pass
        test_oneline.__doc__ = summary + '\n\n' + doc

        with self.assertWarnsRegex(DeprecationWarning, 'get_summaryf'):
            self.ds.get_summaryf('test1')(test_oneline)
        self.assertEqual(self.ds.params['test1.summary'], summary)


    def test_get_extended_summary(self):
        """Test whether the extended summary is extracted correctly"""

        doc = (
            random_text + '\n\n' + parameters_header + '\n' + complex_param)

        def test_basic():
            pass
        test_basic.__doc__ = summary + '\n\n' + doc

        with self.assertWarnsRegex(DeprecationWarning,
                                   'get_extended_summaryf'):
            self.ds.get_extended_summaryf('test1')(test_basic)
        self.assertEqual(self.ds.params['test1.summary_ext'],
                         random_text.strip())

    def test_get_full_description(self):
        """Test whether the full description is extracted correctly"""

        doc = (
            random_text + '\n\n' + parameters_header + '\n' + complex_param)

        def test_basic():
            pass
        test_basic.__doc__ = summary + '\n\n' + doc

        with self.assertWarnsRegex(DeprecationWarning,
                                   'get_full_descriptionf'):
            self.ds.get_full_descriptionf('test1')(test_basic)
        self.assertEqual(self.ds.params['test1.full_desc'],
                         summary + '\n\n' + random_text.strip())

    def test_save_docstring(self):
        """Test the :meth:`docrep.DocstringProcessor.save_docstring` method"""
        def test():
            "Just a test\n\nwith something"
            pass

        with self.assertWarnsRegex(DeprecationWarning, 'save_docstring'):
            self.ds.save_docstring('test')(test)

        self.assertEqual(self.ds.params['test'],
                         "Just a test\n\nwith something")




if __name__ == '__main__':
    unittest.main()
