TryingSnake
-----------

[![Build Status](https://travis-ci.org/zero323/tryingsnake.svg?branch=master)](https://travis-ci.org/zero323/tryingsnake)
[![Coverage Status](https://coveralls.io/repos/zero323/tryingsnake/badge.svg?branch=master&service=github)](https://coveralls.io/github/zero323/tryingsnake?branch=master)
[![PyPI version](https://badge.fury.io/py/tryingsnake.svg)](https://badge.fury.io/py/tryingsnake)

A simple, `Try` implementation inspired by [`scala.util.Try`](http://www.scala-lang.org/files/archive/nightly/docs/library/index.html#scala.util.Try)

Examples
--------

```python
>>> from tryingsnake import Try, Success, Failure

>>> Try(lambda: 1)
Success(1)
>>> Try(lambda: 1 / 0)
Failure(ZeroDivisionError('integer division or modulo by zero',))

>>> def inc(x): return x + 1
>>> Success(1).map(inc)
Success(2)
>>> Failure(Exception("e")).map(inc)
Failure(Exception('e',))

>>> from operator import truediv
>>> Try(truediv, 1, 0).orElse(Success(0))
Success(0)
```
    
LICENSE
-------
MIT, See [LICENSE](https://github.com/zero323/tryingsnake/blob/master/LICENSE)


