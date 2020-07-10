"""Decorator functions for overloaded and deprecated methods"""
import six
from warnings import warn
from functools import wraps


def updates_docstring(func):
    """Decorate a method that updates the docstring of a function."""

    @wraps(func)
    def update_docstring(self, *args, **kwargs):
        if not len(args) or isinstance(args[0], six.string_types):
            return func(self, *args, **kwargs)
        elif len(args) and callable(args[0]):
            doc = func(self, args[0].__doc__, *args[1:], **kwargs)
            args[0].__doc__ = doc
            return args[0]
        else:
            def decorator(f):
                doc = func(self, f.__doc__, *args, **kwargs)
                f.__doc__ = doc
                return f
            return decorator

    return update_docstring


def reads_docstring(func):
    """Decorate a method that accepts a string or function."""

    @wraps(func)
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


def deprecated_method(replacement, replace=True, replacement_name=None):
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

    def decorate(func):

        msg = "The %s method is deprecated, use the %s method instead" % (
            func.__name__,
            replacement_name or getattr(replacement, '__name__', replacement))

        @wraps(func)
        def deprecated(self, *args, **kwargs):
            warn(msg, DeprecationWarning, stacklevel=2)
            if callable(replacement) and replace:
                return replacement(*args, **kwargs)
            elif replace:
                return getattr(self, replacement)(*args, **kwargs)
            else:
                return func(self, *args, **kwargs)

        return deprecated

    return decorate


def deprecated_function(replacement, replace=True, replacement_name=None):
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

    def decorate(func):

        msg = "The %s function is deprecated, use the %s method instead" % (
            func.__name__, replacement_name or replacement.__name__)

        @wraps(func)
        def deprecated(*args, **kwargs):
            warn(msg, DeprecationWarning, stacklevel=2)
            if replace:
                return replacement(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return deprecated

    return decorate