from operator import add, truediv
import unittest
import pytest
from tryingsnake import Try_, Try, Success, Failure


class TryTestCase(unittest.TestCase):
    def test_failure_should_be_failure(self):
        failure = Try(truediv, 1, 0)
        self.assertTrue(failure.isFailure)
        self.assertFalse(failure.isSuccess)

    def test_success_should_be_success(self):
        success = Try(add, "foo", "bar")
        self.assertFalse(success.isFailure)
        self.assertTrue(success.isSuccess)

    def test_failure_should_raise_an_exception_if_created_from_non_exception(self):
        self.assertRaises(TypeError, Failure, 1)

    def test_get_should_raise_an_exception_if_failure(self):
        self.assertRaises(ZeroDivisionError, Try(truediv, 1, 0).get)
        self.assertRaises(TypeError, Try(add, "1", 0).get)

    def test_get_should_return_value_if_success(self):
        self.assertEqual(Try(truediv, 4, 2).get(), 2)
        self.assertEqual(Try(add, "1", "2").get(), "12")

    def test_repr(self):
        def fail():
            raise Exception("failure")

        self.assertEqual(repr(Try(add, 1, 0)), "Success(1)")
        self.assertEqual(
            repr(Try(fail)), "Failure({})".format(repr(Exception("failure")))
        )

    def test_flatmap_on_failure_should_return_failure(self):
        self.assertTrue(Failure(Exception("")).flatMap(lambda x: Success(1)).isFailure)

    def test_flatmap_on_success_should_return_value_depending_on_a_function(self):
        self.assertTrue(Success(1).flatMap(lambda x: Success(1)).isSuccess)
        self.assertTrue(Success(1).flatMap(lambda x: Failure(Exception())).isFailure)

    def test_flatmap_should_fail_if_f_doesnt_return_try(self):
        self.assertRaises(TypeError, Success(1).flatMap, lambda x: x)

    def test_map_on_failure_should_return_failure(self):
        self.assertTrue(Failure(Exception("")).map(lambda x: 1).isFailure)

    def test_map_on_success_should_return_value_depending_on_a_function(self):
        success = Success(1).map(lambda x: -x)
        self.assertTrue(success.isSuccess)
        self.assertEqual(success.get(), -1)

    def test_filter_on_failure_should_return_failure(self):
        self.assertTrue(Failure(Exception("")).filter(lambda x: True).isFailure)
        self.assertTrue(Failure(Exception("")).filter(lambda x: False).isFailure)

    def test_filter_on_success_should_return_value_depending_on_a_predicate(self):
        self.assertTrue(Success(1).filter(lambda x: x > 0).isSuccess)
        self.assertTrue(Success(-1).filter(lambda x: x > 0).isFailure)

    def test_filter_should_accept_custom_exception_and_message(self):
        class DummyException(Exception):
            pass

        failure = Success(1).filter(lambda x: False, DummyException, "dummy")
        self.assertRaises(DummyException, failure.get)
        self.assertEqual(
            repr(failure), "Failure({})".format(repr(DummyException("dummy")))
        )

    def test_recover_on_failure_should_return_value_depending_on_f(self):
        failure = Failure(Exception("e"))
        self.assertTrue(failure.recover(lambda x: 1 / 0).isFailure)
        self.assertTrue(failure.recover(lambda x: 1).isSuccess)

    def test_recover_on_success_should_return_identity(self):
        success = Success(1)
        self.assertEqual(success.recover(lambda x: 1 / 0), success)

    def test_recover_with_on_failure_should_return_value_depending_on_f(self):
        failure = Failure(Exception("e"))
        self.assertTrue(failure.recoverWith(lambda x: Try(lambda: 1 / 0)).isFailure)
        self.assertTrue(failure.recoverWith(lambda x: Try(lambda: 1)).isSuccess)

    def test_recover_with_on_success_should_return_identity(self):
        success = Success(1)
        self.assertEqual(success.recoverWith(lambda x: Try(lambda x: -1)), success)

    def test_recover_with_should_throw_an_exception_f_doesnt_return_try(self):
        self.assertRaises(TypeError, Failure(Exception("e")).recoverWith, lambda x: 1)

    def test_get_or_else_with_success_should_return_this_value(self):
        self.assertEqual(Success(1).getOrElse(lambda: -1), 1)

    def test_get_or_else_with_failure_should_return_else(self):
        self.assertEqual(Failure(Exception("e")).getOrElse(-1), -1)

    def test_or_else_on_success_should_return_identity(self):
        success = Success(1)
        self.assertEqual(success.orElse(lambda: 1), success)

    def test_or_else_on_failure_should_return_else(self):
        success = Success(1)
        self.assertEqual(Failure(Exception("e")).orElse(success), success)

    def test_or_else_on_failure_should_throw_an_exception_default_is_not_try(self):
        self.assertRaises(TypeError, Failure(Exception("e")).orElse, 1)

    def test_failed_on_failure_should_return_success_of_exception(self):
        result = Failure(Exception("e")).failed()
        self.assertTrue(result.isSuccess and isinstance(result.get(), Exception))

    def test_failed_on_success_should_be_a_failure(self):
        result = Success(1).failed()
        self.assertTrue(result.isFailure)

    def test__try_raise_if_not_exception(self):
        self.assertRaises(TypeError, Try_._raise_if_not_exception, 1)
        self.assertIsNone(Try_._raise_if_not_exception(Exception("e")))

    def test__try_identity_if_try_or_raise(self):
        success = Success(1)
        failure = Failure(Exception("e"))
        self.assertRaises(TypeError, Try_._identity_if_try_or_raise, 1)
        self.assertEqual(Try_._identity_if_try_or_raise(success), success)
        self.assertEqual(Try_._identity_if_try_or_raise(failure), failure)

    def test_equality_of_success_should_be_based_on_the_equality_of_values(self):
        self.assertEqual(Success(1), Success(1))
        self.assertNotEqual(Success(1), Success(2))

    def test_equality_of_failure_should_be_based_on_a_type_and_args(self):
        self.assertEqual(Failure(Exception("e")), Failure(Exception("e")))
        self.assertNotEqual(Failure(Exception("foo")), Failure(Exception("bar")))
        self.assertNotEqual(Failure(ZeroDivisionError()), Failure(TypeError()))
        self.assertNotEqual(Failure(Exception("e")), Failure(TypeError("e")))
        self.assertNotEqual(Failure(Exception()), Success(1))

    def test_set_unchecked_should_correctly_set_and_unset_unchecked_exceptions(self):
        from operator import getitem

        Try_.set_unhandled([IndexError])
        self.assertRaises(IndexError, Try, getitem, [1], 3)
        Try_.set_unhandled()
        self.assertTrue(Try(getitem, [1], 3).isFailure)

    def test_truthness(self):
        self.assertFalse(Failure(Exception("e")))
        self.assertTrue(Success(1))

    def test_hashable(self):
        self.assertTrue(hash(Success(1)) == hash(Success(1)))
        self.assertTrue(hash(Success(1)) == 1)
        e = Exception("e")
        self.assertTrue(hash(Failure(e)) == hash(Failure(e)))

    def test_fail_with_unhashable_value(self):
        with pytest.raises(TypeError):
            hash(Success([1]))

        class UnhashableException(Exception):
            def __hash__(self):
                raise TypeError()

        with pytest.raises(TypeError):
            hash(Failure(UnhashableException()))

    def test_generator_without_arguments(self):
        g = (lambda: (yield 1))()
        self.assertEqual(Try(g).map(lambda x: x + 1), Success(2))

    def test_generator_with_argument(self):
        def f():
            x = None
            while True:
                x = yield x

        g = f()
        g.send(None)
        self.assertEqual(Try(g, 41).map(lambda x: x + 1), Success(42))

    def test_generator_failure_with_arguments(self):
        g = (lambda: (yield 1))()

        self.assertTrue(Try(g, a=1).map(lambda x: x + 1).isFailure)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
