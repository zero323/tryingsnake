TryingSnake
===========

[![Build
Status](https://travis-ci.org/zero323/tryingsnake.svg?branch=master)](https://travis-ci.org/zero323/tryingsnake)
[![Coverage
Status](https://coveralls.io/repos/zero323/tryingsnake/badge.svg?branch=master&service=github)](https://coveralls.io/github/zero323/tryingsnake?branch=master)
[![Code
Climate](https://codeclimate.com/github/zero323/tryingsnake/badges/gpa.svg)](https://codeclimate.com/github/zero323/tryingsnake)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/zero323/tryingsnake)](https://github.com/zero323/tryingsnake/releases/latest)
[![PyPI](https://img.shields.io/pypi/v/tryingsnake?color=blue)](https://pypi.org/project/tryingsnake/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/tryingsnake.svg?color=blue)](https://anaconda.org/conda-forge/tryingsnake)
[![License
MIT](https://img.shields.io/pypi/l/tryingsnake.svg)](https://github.com/zero323/tryingsnake/blob/master/LICENSE)

A simple, `Try` implementation inspired by
[scala.util.Try](https://www.scala-lang.org/api/current/scala/util/Try.html)

Examples
========

-   Wrap functions with arguments:

    ```python
    >>> from tryingsnake import Try, Try_, Success, Failure
    >>> from operator import add, truediv
    >>> Try(add, 0, 1)
    Success(1)
    >>> Try(truediv, 1, 0)  # doctest:+ELLIPSIS
    Failure(ZeroDivisionError(...))
    ```

-   Avoid sentinel values:

    ```python
    >>> def mean_1(xs):
    ...     try:
    ...         return sum(xs) / len(xs)
    ...     except ZeroDivisionError as e:
    ...         return float("inf")  # What does it mean?
    >>> mean_1([])
    inf
    ```

    vs.

    ```python
    >>> def mean_2(xs):
    ...     return sum(xs) / len(xs)
    >>> Try(mean_2, [])  # doctest:+ELLIPSIS
    Failure(ZeroDivisionError(...))
    >>> Try(mean_2, ["foo", "bar"])  # doctest:+ELLIPSIS
    Failure(TypeError(...))
    ```

-   Follow the happy path:

    ```python
    >>> def inc(x): return x + 1
    >>> def inv(x): return 1. / x

    >>> Success(1).map(inc).map(inv)
    Success(0.5)

    >>> Failure(Exception("e")).map(inc).map(inv)  # doctest:+ELLIPSIS
    Failure(Exception(...))

    >>> Success(-1).map(inc).map(inv)  # doctest:+ELLIPSIS
    Failure(ZeroDivisionError(...))
    ```

-   Recover:

    ```python
    >>> def get(url):
    ...     if "mirror" in url:
    ...         raise IOError("No address associated with hostname")
    ...     return url
    >>> mirrors = ["http://mirror1.example.com", "http://example.com"]
    >>> Try(get, mirrors[0]).recover(lambda _: get(mirrors[1]))
    Success('http://example.com')
    ```

-   Let them fail:

    ```python
    >>> from operator import getitem
    >>> Try(getitem, [], 0)  # doctest:+ELLIPSIS
    Failure(IndexError(...))
    >>> Try_.set_unhandled([IndexError])
    >>> Try(getitem, [], 0)
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    ```

-   Make things (relatively) simple:

    ```python
    >>> import math
    >>> xs = [1.0, 0.0, "-1", -3, 2, 1 + 2j]
    >>> sqrts = [Try(math.sqrt, x) for x in xs]
    >>> [x.get() for x in sqrts if x.isSuccess]
    [1.0, 0.0, 1.4142135623730951]
    >>> def get_etype(e):
    ...     return Try(lambda x: type(x).__name__, e)
    >>> [x.recoverWith(get_etype).get() for x in sqrts if x.isFailure]
    ['TypeError', 'ValueError', 'TypeError']
    ```

-   Inline exception handling:

    ```python
    >>> from tryingsnake.curried import Try
    >>> map(Try(str.split), ["foo bar", None])  # doctest:+ELLIPSIS
    <map at ...>
    ```

-   Decorate your functions:

    ```python
    >>> from tryingsnake.curried import Try as try_
    >>> @try_
    ... def scale_imag(x):
    ...     return complex(x.real, x.imag * 2)
    >>> [scale_imag(x) for x in [1 + 2j, "3", 42 + 0j]]
    [Success((1+4j)), Failure(AttributeError("'str' object has no attribute 'real'")), Success((42+0j))]
    ```

-   Wrap generator objects:

    ```python
    >>> def get_nth(xs, i):
    ...     yield xs[i]
    >>> xs = [1, 3, 5, 7]
    >>> Try(get_nth(xs, 3))
    Success(7)
    >>> Try(get_nth(xs, 11))
    Failure(IndexError('list index out of range'))
    >>> def f():
    ...     divisor = 1
    ...     while True:
    ...         divisor_ = yield 1 / divisor
    ...         divisor = divisor_ if divisor_ is not None else 1
    >>> g = f()
    >>> next(g)  # Should be primed
    1.0
    >>> Try(g, 2)
    Success(0.5)
    >>> Try(g, 0)
    Failure(ZeroDivisionError('division by zero'))
    ```

Installation
============

This package is available on PYPI:

    pip install tryingsnake

and conda-forge:

    conda install -c conda-forge tryingsnake


Dependencies
=======

`tryingsnake` supports Python 3.6 or later and
requires no external dependencies.

License
=======

MIT, See
[LICENSE](https://github.com/zero323/tryingsnake/blob/master/LICENSE)

FAQ
===

-   Q: Is this project production-ready?
-   A: Sure, for some definition of production-ready. It is a toy project.
    It has decent test coverage, stable API, and in general seems to do
    what is expected to do. But it is not widely used, and the API design
    and overall idea are rather unpythonic.
-   Q: Why to use mixedCase method names instead of lowercase
    recommended by PEP8?
-   A: Mostly to make switching between Python and Scala code as
    painless as possible.
-   Q: What is the runtime cost?    
    A: As of [0088286](https://github.com/zero323/tryingsnake/commit/00882862d655cd3d77ea730449f498883ed584d5) (releases 0.3 and 0.4 suffered from
    severe performance regression caused by using `typing.Generic` as a base of
    try. See [#18](https://github.com/zero323/tryingsnake/issues/18) for details)
    rough numbers for simple tasks look as follows:

    ```
    Python 3.7.5 (default, Oct 27 2019, 15:43:29)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.11.0 -- An enhanced Interactive Python. Type '?' for help.
    In [1]: def identity(x): return x
    In [2]: from tryingsnake import Try
    In [3]: %timeit for i in range(1_000_000): identity(i)
    59.8 ms ± 683 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

    In [4]: %timeit for i in range(1_000_000): Try(identity, i)
    408 ms ± 4.14 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    ```

    and execution time is dominated by the initializer:

    ```
    In [5]: import cProfile
    In [6]: cProfile.run("for i in range(1_000_000): Try(identity, i)")
             4000003 function calls in 0.961 seconds

       Ordered by: standard name

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      1000000    0.078    0.000    0.078    0.000 <ipython-input-1-abafd771428d>:1(identity)
            1    0.263    0.263    0.961    0.961 <string>:1(<module>)
      1000000    0.094    0.000    0.094    0.000 __init__.py:234(__init__)
      1000000    0.480    0.000    0.698    0.000 __init__.py:352(Try)
      1000000    0.046    0.000    0.046    0.000 {built-in method builtins.callable}
            1    0.000    0.000    0.961    0.961 {built-in method builtins.exec}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
    ```

    This is quite a lot for simple functions so you should probably avoid it in such cases, where raw performance is important. It is still possible to amortize the cost in such cases, for example using composition:

    ```python
    from toolz.functoolz import compose
    from tryingsnake import Try

    Try(compose(str.split, str.lower, str.strip), " Foo BAR FooBar ")
    ```

    Memory overhead (as measured by [memory-profiler](https://pypi.org/project/memory-profiler/)) looks as follows:

    ```
    Line #    Mem usage    Increment   Line Contents
    ================================================
     6     37.9 MiB     37.9 MiB   @profile
     7                             def f():
     8    155.5 MiB      0.8 MiB       [Try(identity, i) for i in range(1_000_000)]
    ```

    compared to:

    ```
    Line #    Mem usage    Increment   Line Contents
    ================================================
     6     37.9 MiB     37.9 MiB   @profile
     7                             def f():
     8     77.4 MiB      1.0 MiB       [identity(i) for i in range(1_000_000)]
     ```
