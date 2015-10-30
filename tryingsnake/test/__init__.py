import unittest
from operator import add, truediv
from tryingsnake import _Try, Try, Success, Failure


class TryTestCase(unittest.TestCase):
    def test_failure_should_be_failure(self):
        self.assertTrue(Try(truediv, 1, 0).isFailure)
        self.assertFalse(Try(truediv, 1, 0).isSuccess)

    def test_success_should_be_success(self):
        self.assertFalse(Try(add, 1, -1).isFailure)
        self.assertTrue(Try(truediv, 1, -1).isSuccess)

    def test_failure_should_raise_an_exception_if_created_from_non_exception(self):
        self.assertRaises(TypeError,)

    def test_get_should_raise_an_exception_if_failure(self):
        self.assertRaises(ZeroDivisionError, Try(truediv, 1, 0).get)
        self.assertRaises(TypeError, Try(add, "1", 0).get)

    def test_get_should_return_value_if_success(self):
        self.assertEqual(Try(truediv, 4, 2).get(), 2)
        self.assertEqual(Try(add, "1", "2").get(), "12")

    def test_repr(self):
        def fail(): raise Exception("failure")
        self.assertEqual(repr(Try(add, 1, 0)), "Success(1)")
        self.assertEqual(repr(Try(fail)), "Failure(Exception('failure',))")

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
        class DummyException(Exception): pass
        failure = Success(1).filter(lambda x: False, DummyException, "dummy")
        self.assertRaises(DummyException, failure.get)
        self.assertEqual(repr(failure), "Failure(DummyException('dummy',))")

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

    def test_failed_on_failure_should_throw_stored_exception(self):
        self.assertRaises(Exception, Failure(Exception("e")).failed)

    def test_failed_on_success_should_throw_type_error_exception(self):
        self.assertRaises(TypeError, Success(1).failed)

    def test__try_raise_if_not_exception(self):
        self.assertRaises(TypeError, _Try._raise_if_not_exception, 1)
        self.assertTrue(_Try._raise_if_not_exception(Exception("e")))

    def test__try_identity_if_try_or_raise(self):
        success = Success(1)
        failure = Failure(Exception("e"))
        self.assertRaises(TypeError, _Try._identity_if_try_or_raise, None)
        self.assertEqual(_Try._identity_if_try_or_raise(success), success)
        self.assertEqual(_Try._identity_if_try_or_raise(failure), failure)


if __name__ == '__main__':
    unittest.main()
