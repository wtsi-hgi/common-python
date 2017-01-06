from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Dict, Iterable, Type
from unittest import TestCase

TypeToTest = TypeVar("TestType")


class TestUsingType(Generic[TypeToTest], TestCase, metaclass=ABCMeta):
    """
    TODO
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
