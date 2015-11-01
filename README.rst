TryingSnake
===========

|Build Status| |Coverage Status| |Codacy| |Code Climate| |PyPI version| |License MIT|

A simple, ``Try`` implementation inspired by
`scala.util.Try <http://www.scala-lang.org/files/archive/nightly/docs/library/index.html#scala.util.Try>`__

Examples
========

-  Wrap functions with arguments:

   .. code:: python

       >>> from tryingsnake import Try, Try_, Success, Failure
       >>> from operator import div, add
       >>> Try(add, 0, 1)
       Success(1)
       >>> Try(div, 1, 0)  # doctest:+ELLIPSIS
       Failure(ZeroDivisionError(...))

-  Avoid sentinel values:

   .. code:: python

       >>> def mean_1(xs):
       ...     try:
       ...         return sum(xs) / len(xs)
       ...     except ZeroDivisionError as e:
       ...         return float("inf")  # What does it mean?
       >>> mean_1([])
       inf

   vs.

   .. code:: python

       >>> def mean_2(xs):
       ...     return sum(xs) / len(xs)
       >>> Try(mean_2, [])  # doctest:+ELLIPSIS
       Failure(ZeroDivisionError(...))
       >>> Try(mean_2, ["foo", "bar"])  # doctest:+ELLIPSIS
       Failure(TypeError(...))

-  Follow the happy path:

   .. code:: python

       >>> def inc(x): return x + 1
       >>> def inv(x): return 1. / x

       >>> Success(1).map(inc).map(inv)
       Success(0.5)

       >>> Failure(Exception("e")).map(inc).map(inv)
       Failure(Exception('e',))

       >>> Success(-1).map(inc).map(inv)  # doctest:+ELLIPSIS
       Failure(ZeroDivisionError(...))

-  Recover:

   .. code:: python

       >>> def get(url):
       ...     if "mirror" in url:
       ...         raise IOError("No address associated with hostname")
       ...     return url
       >>> mirrors = ["http://mirror1.example.com", "http://example.com"]
       >>> Try(get, mirrors[0]).recover(lambda _: get(mirrors[1]))
       Success('http://example.com')

-  Let them fail:

   .. code:: python

       >>> from operator import getitem
       >>> Try(getitem, [], 0)
       Failure(IndexError('list index out of range',))
       >>> Try_.set_unhandled([IndexError])
       >>> Try(getitem, [], 0)
       Traceback (most recent call last):
           ...
       IndexError: list index out of range

-  Make things (relatively) simple

   .. code:: python

       >>> import math
       >>> xs = [1.0, 0.0, "-1", -3, 2, 1 + 2j]
       >>> sqrts = [Try(math.sqrt, x) for x in xs]
       >>> [x.get() for x in sqrts if x.isSuccess]
       [1.0, 0.0, 1.4142135623730951]
       >>> def get_etype(e):
       ...     return Try(lambda x: type(x).__name__, e)
       >>> [x.recoverWith(get_etype).get() for x in sqrts if x.isFailure]
       ['TypeError', 'ValueError', 'TypeError']

Installation
============

::

    pip install tryingsnake

or

::

    easy_install tryingsnake

License
=======

MIT, See
`LICENSE <https://github.com/zero323/tryingsnake/blob/master/LICENSE>`__

FAQ
===

-  Q: Is this project production-ready?
-  A: No, and it probably won't be.
-  Q: Why to use mixedCase method names instead of lowercase recommended
   by PEP8?
-  A: Mostly to make switching between Python and Scala code as painless
   as possible.

.. |Build Status| image:: https://travis-ci.org/zero323/tryingsnake.svg?branch=master
   :target: https://travis-ci.org/zero323/tryingsnake
.. |Coverage Status| image:: https://coveralls.io/repos/zero323/tryingsnake/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/zero323/tryingsnake?branch=master
.. |PyPI version| image:: https://badge.fury.io/py/tryingsnake.svg
   :target: https://badge.fury.io/py/tryingsnake
.. |Code Climate| image:: https://img.shields.io/codeclimate/github/zero323/tryingsnake.svg
   :target: https://codeclimate.com/github/zero323/tryingsnake
.. |Codacy| image:: https://img.shields.io/codacy/abef208bba70444d9b5cf0d851ca6c6e.svg
   :target: https://www.codacy.com/app/matthew-szymkiewicz/tryingsnake
.. |License MIT| image:: https://img.shields.io/pypi/l/tryingsnake.svg
   :target: https://github.com/zero323/tryingsnake/blob/master/LICENSE
