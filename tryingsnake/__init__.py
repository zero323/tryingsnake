# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import
import inspect as _inspect


class _Try(object):
    @staticmethod
    def _identity_if_try_or_raise(v, msg="Invalid return type for f: {0}"):
        if not isinstance(v, _Try):
            raise TypeError(msg.format(type(v)))
        return v

    @property
    def isFailure(self):
        """Check if this is a Failure.

        >>> Success(1).isFailure
        False
        >>> Failure(Exception()).isFailure
        True
        """
        return not self._isSuccess

    @property
    def isSuccess(self):
        """Check if this is a Success.

        >>> Success(1).isSuccess
        True
        >>> Failure(Exception()).isSuccess
        False
        """
        return self._isSuccess

    def flatMap(self, f):
        """ Apply potentially function  returning _Try to the value.

        :param f: function to be applied.
        :return: self if this is a Failure otherwise f applied to self.get
        """
        raise NotImplementedError

    def map(self, f):
        """Apply function to the value.

        :param f: function to be applied
        :return: self if this is a Failure otherwise Try(f, self.get)
        """
        return NotImplementedError

    def filter(self, f, exception_cls=Exception, msg=None):
        """Convert this to Failure if f(self.get()) evaluates to False

        :param f:
        :param exception_cls: optional exception class to return
        :param msg: optional message
        :return: self if f evaluates to True otherwise Failure
        """
        raise NotImplementedError

    def recover(self, f):
        raise NotImplementedError

    def recoverWith(self, f):
        raise NotImplementedError

    def failed(self):
        raise NotImplementedError

    def __repr__(self):
        return self._fmt.format(repr(self._v))


class Failure(_Try):
    def __init__(self, e):
        if Exception not in _inspect.getmro(e.__class__):
            msg = "Invalid type for Failure: {0}"
            raise TypeError(msg.format(type(e)))

        self._v = e
        self._isSuccess = False
        self._fmt = "Failure({0})"

    def get(self): raise self._v

    def getOrElse(self, default):
        return default

    def orElse(self, default):
        return _Try._identity_if_try_or_raise(default)

    def map(self, f):
        return self

    def flatMap(self, f):
        return self

    def filter(self, f, exception_cls=Exception, msg=None):
        return self

    def recover(self, f):
        return Try(f, self._v)

    def recoverWith(self, f):
        v = Try(f, self._v)
        return _Try._identity_if_try_or_raise(v if v.isFailure else v.get())

    def failed(self):
        return self.get()


class Success(_Try):
    def __init__(self, v):
        self._v = v
        self._isSuccess = True
        self._fmt = "Success({0})"

    def get(self): return self._v

    def getOrElse(self, default): return self.get()

    def orElse(self, defualt): return self

    def map(self, f):
        return Try(f, self._v)

    def flatMap(self, f):
        v = Try(f, self._v)
        return _Try._identity_if_try_or_raise(v if v.isFailure else v.get())

    def filter(self, f, exception_cls=Exception, msg=None):
        return (self if f(self.get())
                else Failure(exception_cls(msg if msg else repr(f))))

    def recover(self, f):
        return self

    def recoverWith(self, f):
        return self

    def failed(self):
        raise TypeError("Cannot fail Success")


def Try(f, *args, **kwargs):
    """Calls f with provided arguments and wraps the result
    using either Success or Failure.

    :param f: Callable which should be evaluated
    :param args: args which should be passed to f
    :param kwargs: kwargs which should be passed to f
    :return: Either success or Failure

    >>> from operator import add, div
    >>> Try(div, 1L, 0L)
    Failure(ZeroDivisionError('long division or modulo by zero',))
    >>> Try(add, 1L, 2L)
    Success(3L)
    """
    try:
        return Success(f(*args, **kwargs))
    except Exception as e:
        return Failure(e)
