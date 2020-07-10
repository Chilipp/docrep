"""Decorator functions for overloaded and deprecated methods"""
import six
import types
import inspect
from warnings import warn
import functools


deprecated_doc = """
    Deprecated {type}

    .. deprecated:: {version}

        Use :{type_short}:`{replacement}` instead!
"""


def updates_docstring(func):
    """Decorate a method that updates the docstring of a function."""

    @functools.wraps(func)
    def update_docstring(self, *args, **kwargs):
        if not len(args) or isinstance(args[0], six.string_types):
            return func(self, *args, **kwargs)
        elif len(args) and callable(args[0]):
            doc = func(self, args[0].__doc__, *args[1:], **kwargs)
            _set_object_doc(args[0], doc, py2_class=self.python2_classes)
            return args[0]
        else:
            def decorator(f):
                doc = func(self, f.__doc__, *args, **kwargs)
                _set_object_doc(f, doc, py2_class=self.python2_classes)
                return f
            return decorator

    return update_docstring


def reads_docstring(func):
    """Decorate a method that accepts a string or function."""

    @functools.wraps(func)
    def use_docstring(self, s=None, base=None, *args, **kwargs):
        # if only the base key is provided, use this method
        if s:
            if callable(s):
                return func(self, s.__doc__, base, *args, **kwargs)
            else:
                return func(self, s, base, *args, **kwargs)
        elif base:

            def decorator(f):
                func(self, f.__doc__, base, *args, **kwargs)

            return decorator
        else:
            return func(self, s, base, *args, **kwargs)

    return use_docstring


def deprecated_method(replacement, version, replace=True,
                      replacement_name=None):
    """Mark a method as deprecated.

    Parameters
    ----------
    replacement: str or callable
        The name of the method that replaces this one here, or the function
        itself
    replace: bool
        If True, then the `replacement` method is called instead of the
        original one
    replacement_name: str
        The name of the replacement function to use in the warning message
    """

    replacement_name = replacement_name or getattr(
        replacement, '__name__', replacement)

    def decorate(func):

        msg = "The %s method is deprecated, use the %s method instead" % (
            func.__name__, replacement_name)

        def deprecated(self, *args, **kwargs):
            warn(msg, DeprecationWarning, stacklevel=2)
            if callable(replacement) and replace:
                return replacement(*args, **kwargs)
            elif replace:
                return getattr(self, replacement)(*args, **kwargs)
            else:
                return func(self, *args, **kwargs)

        deprecated.__doc__ = deprecated_doc.format(
            type="method", version=version, replacement=replacement_name,
            type_short="meth")

        return functools.wraps(
            func, assigned=set(functools.WRAPPER_ASSIGNMENTS) - {'__doc__'})(
                deprecated)

    return decorate


def deprecated_function(replacement, version, replace=True,
                        replacement_name=None):
    """Mark a method as deprecated.

    Parameters
    ----------
    replacement: callable
        A function to call instead, in case `replace` is True
    replace: bool
        Whether to replace the call of the function with a call of
        `replacement`
    replacement_name: str
        The name of the `replacement` function. If this is None,
        `replacement.__name__` is used
    """

    replacement_name = replacement_name or replacement.__name__

    def decorate(func):

        msg = "The %s function is deprecated, use the %s method instead" % (
            func.__name__, replacement_name)

        def deprecated(*args, **kwargs):
            warn(msg, DeprecationWarning, stacklevel=2)
            if replace:
                return replacement(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        deprecated.__doc__ = deprecated_doc.format(
            type="function", version=version, replacement=replacement_name,
            type_short="func")

        return functools.wraps(
            func, assigned=set(functools.WRAPPER_ASSIGNMENTS) - {'__doc__'})(
                deprecated)

    return decorate


def _set_object_doc(obj, doc, stacklevel=3, py2_class='warn'):
    warn("The DocstringProcessor._set_object_doc method has been "
         "depreceated.", DeprecationWarning)
    if isinstance(obj, types.MethodType) and six.PY2:
        obj = obj.im_func
    try:
        obj.__doc__ = doc
    except AttributeError:  # probably python2 class
        if (py2_class!= 'raise' and
                (inspect.isclass(obj) and six.PY2)):
            if py2_class == 'warn':
                warn("Cannot modify docstring of classes in python2!",
                     stacklevel=stacklevel)
        else:
            raise
    return obj