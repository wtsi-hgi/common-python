from abc import ABCMeta
from collections import Sized

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


class Metadata(Model, Sized):
    """
    Generic key-value metadata model.
    """
    # This is composed from a dictionary, rather than inheriting, in case the implementation needs to change and to
    # expose only the methods used...
    def __init__(self, initial: dict=None):
        self._data = dict()
        if initial is not None:
            for key, value in initial.items():
                self.set(key, value)

    def __iter__(self):
        return self._data.__iter__()

    def has_attribute(self, attribute: str) -> bool:
        """
        Check an attribute exists in the metadata.
        :param attribute: dictionary key
        :return: exists in the dictionary
        """
        return attribute in self._data

    def items(self):
        return self._data.items()

    def attributes(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def get(self, attribute: str, default=None):
        """
        Get item in metadata by its attribute, returning a fallback value when the attribute is not found.
        :param attribute: dictionary key
        :param default: default value, if not found
        :return: the value
        """
        return self._data.get(attribute, default)

    def __getitem__(self, attribute: str):
        return self.get(attribute)

    def set(self, attribute: str, value):
        """
        Set item in metadata by its attribute.
        :param attribute: dictionary key
        :param value: value
        """
        self._data[attribute] = value

    def __setitem__(self, attribute: str, value):
        self.set(attribute, value)

    def __len__(self):
        return len(self._data)
