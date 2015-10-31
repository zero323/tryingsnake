TryingSnake
===========

|Build Status| |Coverage Status| |PyPI version|

A simple, ``Try`` implementation inspired by
`scala.util.Try <http://www.scala-lang.org/files/archive/nightly/docs/library/index.html#scala.util.Try>`__

Examples
========

-  Wrap functions with arguments:

   .. code:: python

       >>> from tryingsnake import Try, Success, Failure

       >>> def succeed(): return 1
       >>> Try(succeed)
       Success(1)

       >>> def fail(): return 1 / 0
       >>> Try(fail)
       Failure(ZeroDivisionError('integer division or modulo by zero',))

-  Avoid sentinel values:

   .. code:: python

       >>> def mean_1(xs):
       ...     try:
       ...       return sum(xs) / len(xs)
       ...     except ZeroDivisionError as e:
       ...         return None
       >>> mean_1([])  # What does it mean?

   vs.

   .. code:: python

       >>> def mean_2(xs): return sum(xs) / len(xs)
       >>> Try(mean_2, [])
       Failure(ZeroDivisionError('integer division or modulo by zero',))
       >>> Try(mean_2, ["foo", "bar"])
       Failure(TypeError("unsupported operand type(s) for +: 'int' and 'str'",))

-  Follow the happy path:

   .. code:: python

       >>> def inc(x): return x + 1
       >>> def inv(x): return 1. / x

       >>> Success(1).map(inc).map(inv)
       Success(0.5)

       >>> Failure(Exception("e")).map(inc).map(inv)
       Failure(Exception('e',))

       >>> Success(-1).map(inc).map(inv)
       Failure(ZeroDivisionError('float division by zero',))

-  Recover:

   .. code:: python

       >>> import urllib
       >>> def get(url): return urllib.urlopen(url).url
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
       IndexError: ...

-  Make things (relatively) simple

   .. code:: python

       >>> import math
       >>> from collections import Counter
       >>> xs = [1.0, 0.0, "-1", -3, 2, 1 + 2j]
       >>> sqrts = [Try(math.sqrt, x) for x in xs]
       >>> [x.get() for x in sqrts if x.isSuccess]
       [1.0, 0.0, 1.4142135623730951]
       >>> def get_etype(x):
       ...     return x.recoverWith(lambda x: Try(type, x)).get()
       >>> Counter(get_etype(x) for x in sqrts if x.isFailure)
       Counter({ValueError: 1, TypeError: 2})

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
-  A: No, and it probablly won't be.
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
