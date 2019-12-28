import tryingsnake


def Try(f):
    """A curried version of Try.

    :param f: Callable[..., T]
    :return: Callable[..., Try_[T]]

    >>> from operator import add, truediv
    >>> try_div = Try(truediv)
    >>> try_div(1, 0)  # doctest:+ELLIPSIS
    Failure(ZeroDivisionError(...))
    >>> try_add = Try(add)
    >>> try_add(1, 2)
    Success(3)
    """

    def _(*args, **kwargs):
        return tryingsnake.Try(f, *args, **kwargs)

    return _
