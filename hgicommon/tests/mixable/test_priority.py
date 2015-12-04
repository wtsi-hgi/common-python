import unittest
from queue import PriorityQueue

from hgicommon.mixable import Priority


class TestPriority(unittest.TestCase):
    """
    Test cases for `Priority`.
    """
    class _MockPriority(Priority):
        pass

    def setUp(self):
        self.low_priority = TestPriority._MockPriority(Priority.MIN_PRIORITY)
        self.medium_priority = TestPriority._MockPriority(Priority.get_lower_priority_value(Priority.MAX_PRIORITY))
        self.high_priority = TestPriority._MockPriority(Priority.MAX_PRIORITY)

    def test_get_lower_priority_value(self):
        lower = Priority.get_lower_priority_value(Priority.MAX_PRIORITY)
        self.assertLess(abs(lower - Priority.MIN_PRIORITY), abs(Priority.MAX_PRIORITY - Priority.MIN_PRIORITY))

    def test_get_lower_priority_value_if_already_minimum(self):
        self.assertRaises(ValueError, Priority.get_lower_priority_value, Priority.MIN_PRIORITY)

    def test_get_higher_priority_value(self):
        higher = Priority.get_higher_priority_value(Priority.MIN_PRIORITY)
        self.assertLess(abs(higher - Priority.MIN_PRIORITY), abs(Priority.MAX_PRIORITY - Priority.MIN_PRIORITY))

    def test_work_in_priority_queue(self):
        queue = PriorityQueue()
        priorities = [self.medium_priority, self.low_priority, self.high_priority]

        for priority in priorities:
            queue.put(priority)

        self.assertListEqual(sorted(priorities), [self.high_priority, self.medium_priority, self.low_priority])
        self.assertEquals(queue.get(), self.high_priority)
        self.assertEquals(queue.get(), self.medium_priority)
        self.assertEquals(queue.get(), self.low_priority)


if __name__ == "__main__":
    unittest.main()
