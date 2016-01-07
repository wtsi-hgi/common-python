from typing import Generic, Sequence, TypeVar, Callable, Optional

_ListenableDataType = TypeVar("ListenableDataType")


class Listenable(Generic[_ListenableDataType]):
    """
    Class on which listeners can be added.
    """
    _PLACEHOLDER = TypeVar("nothing")

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
        Removes a listener.
        :param listener: the event listener to remove
        """
        self._listeners.remove(listener)

    def notify_listeners(self, data: Optional[_ListenableDataType]=_PLACEHOLDER):
        """
        Notify event listeners, passing them the given data (if any).
        :param data: the data to pass to the event listeners
        """
        for listener in self._listeners:
            if data is not Listenable._PLACEHOLDER:
                listener(data)
            else:
                listener()
