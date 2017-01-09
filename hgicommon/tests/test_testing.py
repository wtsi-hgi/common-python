import unittest

from hgicommon.testing import TestUsingType, create_tests, TypeToTest, get_classes_to_test, \
    TEST_LATEST_ONLY_ENVIRONMENT_VARIABLE_SET_VALUE


class TestCreateTests(unittest.TestCase):
    """
    Tests for `create_tests`.
    """
    def test_can_create_tests(self):
        class ExampleTest(TestUsingType[TypeToTest]):
            pass

        test_types = {int, str, float}
        tests = create_tests(ExampleTest, test_types)

        for name, test in tests.items():
            self.assertTrue(issubclass(test, TestUsingType))
            test_types.remove(test.get_type_to_test())
        self.assertEqual(0, len(test_types))


class TestGetClassesToTest(unittest.TestCase):
    """
    Tests for `get_classes_to_test`.
    """
    _ALL_CLASSES = {int, str, float}
    _LATEST_CLASS = str

    def test_all_returned_if_environment_variable_not_set(self):
        assert TEST_LATEST_ONLY_ENVIRONMENT_VARIABLE_SET_VALUE != ""
        to_test = get_classes_to_test(TestGetClassesToTest._ALL_CLASSES, TestGetClassesToTest._LATEST_CLASS,
                                      _environment_variable_reader=lambda str: "")
        self.assertEqual(TestGetClassesToTest._ALL_CLASSES, to_test)

    def test_all_returned_if_environment_variable_set(self):
        to_test = get_classes_to_test(TestGetClassesToTest._ALL_CLASSES, TestGetClassesToTest._LATEST_CLASS,
                                      _environment_variable_reader=lambda str: TEST_LATEST_ONLY_ENVIRONMENT_VARIABLE_SET_VALUE)
        self.assertEqual({TestGetClassesToTest._LATEST_CLASS}, to_test)

    def test_valid_return_given_current_environment_variable_setting(self):
        to_test = get_classes_to_test(TestGetClassesToTest._ALL_CLASSES, TestGetClassesToTest._LATEST_CLASS)
        if len(to_test) == 1:
            self.assertEqual({TestGetClassesToTest._LATEST_CLASS}, to_test)
        else:
            self.assertEqual(TestGetClassesToTest._ALL_CLASSES, to_test)


if __name__ == "__main__":
    unittest.main()
