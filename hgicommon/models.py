from abc import ABCMeta
from typing import Any

import sys

from hgicommon.enums import ComparisonOperator


class Model(metaclass=ABCMeta):
    """
    Superclass that all POPOs (Plain Old Python Objects) must implement.
    """
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for property_name, value in vars(self).items():
            if other.__dict__[property_name] != self.__dict__[property_name]:
                return False
        return True

    def __str__(self) -> str:
        string_builder = []
        for property, value in vars(self).items():
            string_builder.append("%s: %s" % (property, value))
        return "{ %s }" % ', '.join(string_builder)

    def __repr__(self) -> str:
        return "%s %s" % (self.__class__, str(self))

    def __hash__(self):
        return hash(str(self))


class SearchCriterion(Model):
    """
    Model of an attribute search criterion.
    """
    def __init__(self, attribute: str, value: str, comparison_operator: ComparisonOperator):
        self.attribute = attribute
        self.value = value
        self.comparison_operator = comparison_operator


class File(Model):
    """
    Model of a file.
    """
    def __init__(self, directory: str, file_name: str):
        self.directory = directory
        self.file_name = file_name


class Priority(Model, metaclass=ABCMeta):
    """
    A model that has a priority, designed for use in `queue.PriorityQueue`.

    Negative numbers have a higher priority than positive ones.
    """
    _NOT_COMPARABLE = "Can only compare to classes implementing 'Priority'"

    MAX_PRIORITY = -sys.maxsize
    MIN_PRIORITY = sys.maxsize

    @staticmethod
    def get_higher_priority_value(value: int):
        """
        Gets a higher priority value than that given.

        Will raise a `ValueError` if already highest priority value.
        :param value: gets a higher priority value than this
        :return: the higher priority value
        """
        if value == Priority.MAX_PRIORITY:
            raise ValueError("Maximum value already")
        return value - 1

    @staticmethod
    def get_lower_priority_value(value: int):
        """
        Gets a lower priority value than that given.

        Will raise a `ValueError` if already lowest priority value.
        :param value: gets a lower priority value than this
        :return: the lower priority value
        """
        if value == Priority.MIN_PRIORITY:
            raise ValueError("Minimum priority already")
        return value + 1

    def __init__(self, priority: int=MIN_PRIORITY):
        self.priority = priority

    def __lt__(self, other):
        if not issubclass(type(other), Priority):
            raise ValueError(Priority._NOT_COMPARABLE)
        return self.priority < other.priority

    def __le__(self, other):
        if not issubclass(type(other), Priority):
            raise ValueError(Priority._NOT_COMPARABLE)
        return self.priority <= other.priority

    def __eq__(self, other):
        if not issubclass(type(other), Priority):
            raise ValueError(Priority._NOT_COMPARABLE)
        return self.priority == other.priority

    def __ge__(self, other):
        if not issubclass(type(other), Priority):
            raise ValueError(Priority._NOT_COMPARABLE)
        return self.priority >= other.priority

    def __gt__(self, other):
        if not issubclass(type(other), Priority):
            raise ValueError(Priority._NOT_COMPARABLE)
        return self.priority > other.priority
