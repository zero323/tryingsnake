from operator import add, truediv
import unittest
import pytest
from tryingsnake.curried import Try as CurriedTry


class CurriedTryTestCase(unittest.TestCase):
    def test_can_take_args_and_fail(self):
        try_trudiv = CurriedTry(truediv)
        self.assertTrue(try_trudiv(1, 0).isFailure)

    def test_can_take_args_and_succeed(self):
        try_add = CurriedTry(add)
        self.assertTrue(try_add(1, 3).isSuccess)

    def test_can_take_kwargs_and_fail(self):
        def f(a, b):
            return a / b

        try_f = CurriedTry(f)
        self.assertTrue(try_f(a=1, b=0).isFailure)

    def test_can_take_kwargs_and_succeed(self):
        def f(a, b):
            return a + b

        try_f = CurriedTry(f)
        self.assertTrue(try_f(a=1, b=3).isSuccess)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
