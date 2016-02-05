import copy
from collections import defaultdict
from multiprocessing import Lock
from typing import Any, Iterable, Sequence, Mapping, Optional

from hgicommon.enums import ComparisonOperator
from hgicommon.models import SearchCriterion


class SearchCriteria(Sequence):
    """
    A collection of `SearchCriterion`.
    """
    _DUPLICATE_ERROR_MESSAGE = "Search criterion based on the attribute `%s` already added"
    _SENTINEL = SearchCriterion("", "", ComparisonOperator.EQUALS)

    def __init__(self, search_criterions: Iterable[SearchCriterion]=()):
        self._data = []
        for search_criterion in search_criterions:
            self.append(search_criterion)

    def append(self, search_criterion: SearchCriterion):
        """
        Appends a search criterion to this collection.
        :param search_criterion: the search criterion to add
        """
        if self.find_by_attribute(search_criterion.attribute) is not None:
            raise ValueError(SearchCriteria._DUPLICATE_ERROR_MESSAGE)
        self._data.append(search_criterion)

    def extend(self, search_criteria):
        """
        Extend this collection by appending search criterion from another search criteria.
        :param search_criteria: the search criteria to merge
        """
        for search_criteria in search_criteria:
            self.append(search_criteria)

    def pop(self, index: int) -> SearchCriterion:
        """
        Removes the search criterion from this collection at the given index.
        :param index: index of the search criteria to remove
        """
        return self._data.pop(index)

    def find_by_attribute(self, attribute: str) -> Optional[SearchCriterion]:
        """
        Find search criteria in this collection based on the attribute it searches on.
        :param attribute: the search criterion attribute to search on
        :return: the matched search criterion
        """
        for existing_search_criterion in self:
            if existing_search_criterion.attribute == attribute:
                return existing_search_criterion
        return None

    def remove_by_attribute(self, attribute: str):
        """
        Remove search criteria that uses the given attribute from this collection.
        :param attribute: the search criteria attribute to search on
        """
        if self.find_by_attribute(attribute) is None:
            raise ValueError("Search criteria with the given attribute was not found")
        deleted = False
        index = 0
        while not deleted:
            if self[index].attribute == attribute:
                del self[index]
                deleted = True
            index += 1

    def __delitem__(self, index: int):
        del self._data[index]

    def __eq__(self, other: Any) -> bool:
        if type(other) != type(self):
            return False
        return other._data == self._data

    def __iter__(self) -> Iterable[SearchCriterion]:
        return self._data.__iter__()

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int) -> Any:
        return self._data[index]

    def __setitem__(self, index: int, search_criterion: SearchCriterion):
        if len(self._data) <= index:
            raise IndexError("Index out of range")

        # Temp replace current so checking for search criteria with same attribute ignores the value at the replace
        # index
        current_value = self._data[index]
        self._data[index] = SearchCriteria._SENTINEL

        if self.find_by_attribute(search_criterion.attribute):
            self._data[index] = current_value
            raise ValueError(SearchCriteria._DUPLICATE_ERROR_MESSAGE)

        self._data[index] = search_criterion

    def __contains__(self, value: SearchCriterion) -> bool:
        return value in self._data

    def __str__(self):
        return str(self._data)

    def __repr__(self) -> str:
        return "<%s object at %s: %s>" % (type(self), id(self), str(self))


class Metadata(Mapping):
    """
    Generic key-value metadata model.
    """
    def __init__(self, seq=()):
        """
        Constructor.
        :param seq: initial metadata items
        """
        self._data = dict(seq)
        self._key_lock = defaultdict(Lock)    # type: Dict[Any, Lock]

    def rename(self, key: Any, new_key: Any):
        """
        Renames an item in this collection as a transaction.

        Will override if new key name already exists.
        :param key: the current name of the item
        :param new_key: the new name that the item should have
        """
        if new_key == key:
            return

        required_locks = [self._key_lock[key], self._key_lock[new_key]]
        ordered_required_locks = sorted(required_locks, key=lambda x: id(x))
        for lock in ordered_required_locks:
            lock.acquire()

        try:
            if key not in self._data:
                raise KeyError("Attribute to rename \"%s\" does not exist" % key)
            self._data[new_key] = self[key]
            del self._data[key]
        finally:
            for lock in required_locks:
                lock.release()

    def get(self, key: Any, default=None) -> Any:
        return self._data.get(key, default)

    def pop(self, key: Any, default=None) -> Any:
        with self._key_lock[key]:
            value = self.get(key, default)
            del self._data[key]
            return value

    def clear(self):
        for key in self._key_lock.items():
            self[key].acquire()
        self._data.clear()
        for key in self._key_lock.items():
            self[key].release()

    def items(self) -> Iterable(Any):
        return self._data.items()

    def keys(self) -> Iterable(Any):
        return self._data.keys()

    def values(self) -> Iterable(Any):
        return self._data.values()

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return "<%s object at %s: %s>" % (type(self), id(self), str(self))

    def __eq__(self, other: Any) -> bool:
        if type(other) != type(self):
            return False
        return other._data == self._data

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __iter__(self) -> Iterable(Any):
        return self._data.__iter__()

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: Any) -> Any:
        return self._data[key]

    def __setitem__(self, key: Any, value: Any):
        with self._key_lock[key]:
            self._data[key] = value

    def __delitem__(self, key: Any):
        with self._key_lock[key]:
            del self._data[key]

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def __copy__(self):
        return self.__class__(self._data)

    def __deepcopy__(self, memo):
        data_deepcopy = copy.deepcopy(self._data)
        deepcopy = self.__class__(data_deepcopy)
        memo[id(self)] = deepcopy
        return deepcopy
