from abc import ABCMeta
from typing import Generic, Sequence, TypeVar, Callable


_ListenableDataType = TypeVar('_ListenableDataType')


class Listenable(Generic[_ListenableDataType], metaclass=ABCMeta):
    """
    Class on which listeners can be added.
    """
    def __init__(self):
        self._listeners = []

    def get_listeners(self) -> Sequence[Callable[[_ListenableDataType], None]]:
        """
        Get all of the registered listeners.
        :return: list of the registered listeners
        """
        return self._listeners

    def add_listener(self, listener: Callable[[_ListenableDataType], None]):
        """
        Adds a listener.
        :param listener: the event listener
        """
        self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[_ListenableDataType], None]):
        """
        Removes a listener
        :param listener: the event listener to remove
        """
        self._listeners.remove(listener)

    def notify_listeners(self, data: _ListenableDataType):
        """
        Notify event listeners, passing them the given data
        :param data: the data to pass to the event listeners
        """
        for listener in self._listeners:
            listener(data)
