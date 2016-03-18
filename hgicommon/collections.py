import copy
from collections import defaultdict
from threading import Lock
from typing import Any, Iterable, Mapping, Dict


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
            return self._data.pop(key, None)

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
