import os
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Dict, Iterable, Type, Set, Callable
from unittest import TestCase

TEST_LATEST_ONLY_ENVIRONMENT_VARIABLE_NAME = "TEST_LATEST_ONLY"
TEST_LATEST_ONLY_ENVIRONMENT_VARIABLE_SET_VALUE = "1"

TypeToTest = TypeVar("TestType")


class TestUsingType(Generic[TypeToTest], TestCase, metaclass=ABCMeta):
    """
    A test for a type that can be retrieved using the `get_type_to_test` method.
    """
    @staticmethod
    @abstractmethod
    def get_type_to_test() -> TypeToTest:
        """
        Gets the class type being tested
        :return: the type of class to test
        """


def create_tests(superclass: Type[TestUsingType], types: Iterable[type]) -> Dict[str, TestUsingType]:
    """
    Creates tests classes that are subclasses of the given superclass for a number of different types.
    :param superclass: the test superclass (must be a subclass of `TestUsingType`)
    :param types: the types to test
    :return: dictionary with the names of the tests as keys and the tests as values
    """
    tests = dict()      # type: Dict[str, TestCase]
    for test_type in types:
        name = "Test%s" % test_type.__name__
        test = type(
            name,
            (superclass[test_type], ),
            # Confusing lambda magic explained here: http://stackoverflow.com/a/2295368
            {"get_type_to_test": staticmethod((lambda test_type: lambda: test_type)(test_type))}
        )
        tests[name] = test
    return tests


def get_classes_to_test(all_classes: Set[type], latest_class: type,
                        _environment_variable_reader: Callable[[str], str]=os.environ.get) -> Set[type]:
    """
    Gets the classes of all those given that are to be tested, where the environment variable
    `TEST_LATEST_ONLY_ENVIRONMENT_VARIABLE_NAME` can be used to limit testing to the given latest only.
    :param all_classes: all classes that can be tested
    :param latest_class: the latest of the given classes
    :param _environment_variable_reader: not to be used - for use in testing only
    :return: classes to be tested
    """
    test_latest_only = _environment_variable_reader(TEST_LATEST_ONLY_ENVIRONMENT_VARIABLE_NAME)
    if test_latest_only == TEST_LATEST_ONLY_ENVIRONMENT_VARIABLE_SET_VALUE:
        return {latest_class}
    else:
        return all_classes
