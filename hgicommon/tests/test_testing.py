import unittest

from hgicommon.testing import TestUsingType, create_tests, TypeToTest


class TestCreateTests(unittest.TestCase):
    """
    Tests for `create_tests`.
    """
    class _ConcreteTestUsingType(TestUsingType[TypeToTest]):
        """
        Concrete subclass of `TestUsingType`.
        """

    def test_can_create_tests(self):
        test_types = {int, str, float}
        tests = create_tests(TestCreateTests._ConcreteTestUsingType, test_types)

        for name, test in tests.items():
            self.assertTrue(issubclass(test, TestUsingType))
            test_types.remove(test.get_type_to_test())
        self.assertEqual(0, len(test_types))


if __name__ == "__main__":
    unittest.main()
