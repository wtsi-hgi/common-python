from collections import defaultdict
from multiprocessing import Lock
from typing import Any
from typing import Dict
from typing import Sequence

from hgicommon.models import SearchCriterion


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


class Metadata(Dict):
    """
    Generic key-value metadata model.
    """
    def __init__(self, seq=()):
        """
        Constructor.
        :param seq: initial values
        """
        super().__init__(seq)
        self._attribute_lock = defaultdict(Lock)    # type: Dict[Any, Lock]

    def get(self, attribute: Any, default=None):
        """
        Get item in this collection by its attribute, returning a fallback value when the attribute is not found.
        :param attribute: dictionary key
        :param default: default value, if not found
        :return: the value
        """
        return super().get(attribute, default)

    def __getitem__(self, attribute: Any):
        return self.get(attribute)

    def set(self, attribute: Any, value: Any):
        """
        Set item in this collection by its attribute.
        :param attribute: dictionary key
        :param value: value
        """
        super().__setitem__(attribute, value)

    def __setitem__(self, attribute: Any, value: Any):
        self.set(attribute, value)

    def rename(self, attribute: Any, new_attribute: Any):
        """
        Renames an item in this collection as a transaction.

        Will override values if new attribute name already exists.
        :param attribute: the current name of the item
        :param new_attribute: the new name that the item should have
        """
        if new_attribute == attribute:
            return

        required_locks = [self._attribute_lock[attribute], self._attribute_lock[new_attribute]]
        ordered_required_locks = sorted(required_locks, key=lambda x: id(x))
        for lock in ordered_required_locks:
            lock.acquire()

        try:
            if attribute not in self:
                raise KeyError("Attribute to rename \"%s\" does not exist" % attribute)
            self[new_attribute] = self[attribute]
            del self[attribute]
        finally:
            for lock in ordered_required_locks:
                lock.release()
