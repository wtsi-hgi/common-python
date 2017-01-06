import unittest
from typing import Any, Union, Type

from hgicommon.testing import TestUsingType, create_tests, TypeToTest


class TestCreateTests(unittest.TestCase):
    """
    Tests for `create_tests`.
    """
    # class _ConcreteTestUsingType(TestUsingType[TypeToTest]):
    #     """
    #     Concrete subclass of `TestUsingType`.
    #     """

    def test_can_create_tests(self):
        class ExampleTest(TestUsingType[TypeToTest]):
            pass

        test_types = {int, str, float}
        tests = create_tests(ExampleTest, test_types)

        for name, test in tests.items():
            self.assertTrue(issubclass(test, TestUsingType))
            test_types.remove(test.get_type_to_test())
        self.assertEqual(0, len(test_types))


if __name__ == "__main__":
    unittest.main()
