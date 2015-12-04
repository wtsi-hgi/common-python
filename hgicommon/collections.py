from typing import Sequence, Sized

from hgicommon.models import SearchCriterion, Model


class SearchCriteria(list):
    """
    A collection of `SearchCriterion`.
    """
    _DUPLICATE_ERROR_MESSAGE = "Search criterion based on the attribute `%s` already added"

    def __init__(self, search_criterion_list: Sequence[SearchCriterion]=()):
        super(SearchCriteria, self).__init__()
        for search_criterion in search_criterion_list:
            self.append(search_criterion)

    def append(self, search_criterion: SearchCriterion):
        for existing_search_criterion in self:
            if existing_search_criterion.attribute == search_criterion.attribute:
                raise ValueError(SearchCriteria._DUPLICATE_ERROR_MESSAGE)

        super(SearchCriteria, self).append(search_criterion)

    def extend(self, iterable):
        for search_criteria in iterable:
            self.append(search_criteria)

    def __setitem__(self, key, value):
        count = self.count(value)
        if count > 1 or (count == 1 and self.index(value) != key):
            raise ValueError(SearchCriteria._DUPLICATE_ERROR_MESSAGE)
        super(SearchCriteria, self).__setitem__(key, value)

    def __add__(self, other):
        for search_criteria in other:
            self.append(search_criteria)


class Metadata(Sized):
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

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return '{class_id} {representation}'.format(
            class_id = self.__class__,
            representation = str(self)
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._data == other._data

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
