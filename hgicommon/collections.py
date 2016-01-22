from collections import defaultdict
from multiprocessing import Lock
from typing import Any, Iterable, Sized, Dict, Sequence

from hgicommon.models import SearchCriterion


class SearchCriteria(list):
    """
    A collection of `SearchCriterion`.
    """
    _DUPLICATE_ERROR_MESSAGE = "Search criterion based on the attribute `%s` already added"

    def __init__(self, search_criterion_list: Sequence[SearchCriterion]=()):
        super().__init__()
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

    def __repr__(self) -> str:
        return "<%s object at %s: %s>" % (type(self), id(self), str(self))


class Metadata(Sized, Iterable):
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

        Will override values if new key name already exists.
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
