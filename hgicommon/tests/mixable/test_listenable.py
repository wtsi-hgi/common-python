import unittest
from typing import List
from unittest.mock import MagicMock

from hgicommon.mixable.listenable import Listenable


class TestListenable(unittest.TestCase):
    """
    Tests for `Listenable` model.
    """
    class _IntListenable(Listenable[int]):
        pass

    def setUp(self):
        # `self._listenable = Listenable[Int]()` does not seem to work as defined in the specification:
        # https://www.python.org/dev/peps/pep-0484/#instantiating-generic-classes-and-type-erasure
        self._listenable = TestListenable._IntListenable()

    def test_add_listener_and_get_update_listeners(self):
        listeners = TestListenable._add_n_mock_listeners_to_listenable(5, self._listenable)
        self.assertCountEqual(self._listenable.get_listeners(), listeners)

    def test_remove_listener_with_existing_listeners(self):
        listeners = TestListenable._add_n_mock_listeners_to_listenable(5, self._listenable)
        for listener in listeners:
            self._listenable.remove_listener(listener)
        self.assertEquals(len(self._listenable.get_listeners()), 0)

    def test_remove_listener_with_non_existing_listener(self):
        TestListenable._add_n_mock_listeners_to_listenable(5, self._listenable)
        self.assertRaises(ValueError, self._listenable.remove_listener, MagicMock())

    def test_notify_listener(self):
        listeners = TestListenable._add_n_mock_listeners_to_listenable(5, self._listenable)
        self._listenable.notify_listeners(123)
        for listener in listeners:
            listener.assert_called_once_with(123)

    def test_notify_listener_with_no_data(self):
        listenable = Listenable()
        listeners = TestListenable._add_n_mock_listeners_to_listenable(5, listenable)
        listenable.notify_listeners()
        for listener in listeners:
            listener.assert_called_once_with()

    @staticmethod
    def _add_n_mock_listeners_to_listenable(number_of_listeners_to_add: int, listenable: Listenable) -> List[MagicMock]:
        """
        Adds the given number of mock listeners to the given listenable.
        :param number_of_listeners_to_add: the number of mock listeners to add
        :param listenable: the listenable to add the listeners to
        :return: the mock listeners that were added
        """
        listeners = []
        for i in range(number_of_listeners_to_add):
            listener = MagicMock()
            listenable.add_listener(listener)
            listeners.append(listener)
        return listeners


if __name__ == "__main__":
    unittest.main()
