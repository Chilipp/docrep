"""Decorator functions for overloaded and deprecated methods"""
import six
import types
import inspect
from warnings import warn
import functools


deprecated_doc = """
    Deprecated {type}

    .. deprecated:: {version}

        Use :{type_short}:`{replacement}` instead! {removed_in}
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
                return f

            return decorator
        else:
            return func(self, s, base, *args, **kwargs)

    return use_docstring


def deprecated(replacement, version, replace=True, replacement_name=None,
               removed_in=None):
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

        try:
            args = inspect.getfullargspec(func).args
        except AttributeError:  # py27
            args = inspect.getargspec(func).args

        if args and args[0] in ['self', 'cls']:  # assume classmethod or method
            what = 'method'
        else:
            what = 'function'

        msg = "The {name} {type} is deprecated, use the {repl} {type} instead."
        msg = msg.format(name=func.__name__, type=what, repl=replacement_name)

        if removed_in:
            msg += " {name} will be removed in {removed_in}".format(
                name=func.__name__, removed_in=removed_in)

        if what == 'method':

            def deprecated(self, *args, **kwargs):
                warn(msg, DeprecationWarning, stacklevel=2)
                if callable(replacement) and replace:
                    return replacement(*args, **kwargs)
                elif replace:
                    return getattr(self, replacement)(*args, **kwargs)
                else:
                    return func(self, *args, **kwargs)

        else:

            if replace:
                if not callable(replacement):
                    raise ValueError(
                        "Replacement functions for deprecated functions must "
                        "be callable!")

            def deprecated(*args, **kwargs):
                warn(msg, DeprecationWarning, stacklevel=2)
                if replace:
                    return replacement(*args, **kwargs)
                else:
                    return func(*args, **kwargs)

        deprecated.__doc__ = deprecated_doc.format(
            type=what, version=version, replacement=replacement_name,
            type_short=what[:4],
            removed_in=(("It will be removed in version {%s}." % removed_in)
                        if removed_in else ""))

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
