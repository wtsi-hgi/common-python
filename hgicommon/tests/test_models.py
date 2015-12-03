import unittest
from datetime import date
from queue import PriorityQueue

from hgicommon.models import Model, Priority


class _StubModel(Model):
    """
    Stub `Model`.
    """
    def __init__(self):
        super(Model, self).__init__()
        self.property_1 = 1
        self.property_2 = "a"
        self.property_3 = []


class TestModel(unittest.TestCase):
    """
    Test cases for `Model`.
    """
    def setUp(self):
        self._model = _StubModel()

    def test_equal_non_nullity(self):
        self.assertNotEqual(self._model, None)

    def test_equal_different_type(self):
        self.assertNotEqual(self._model, date)

    def test_equal_reflexivity(self):
        model = self._model
        self.assertEqual(model, model)

    def test_equal_symmetry(self):
        model1 = self._model
        model2 = self._model
        self.assertEqual(model1, model2)
        self.assertEqual(model2, model1)

    def test_equal_transitivity(self):
        model1 = self._model
        model2 = self._model
        model3 = self._model
        self.assertEqual(model1, model2)
        self.assertEqual(model2, model3)
        self.assertEqual(model1, model3)

    def test_can_get_string_representation(self):
        string_representation = str(self._model)
        self.assertTrue(isinstance(string_representation, str))


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
        self.assertLess(Priority.MIN_PRIORITY - lower, Priority.MIN_PRIORITY - Priority.MAX_PRIORITY)

    def test_get_lower_priority_value_if_already_minimum(self):
        self.assertRaises(ValueError, Priority.get_lower_priority_value, Priority.MIN_PRIORITY)

    def test_get_higher_priority_value(self):
        higher = Priority.get_higher_priority_value(Priority.MIN_PRIORITY)
        self.assertGreater(Priority.MAX_PRIORITY - higher, Priority.MAX_PRIORITY - Priority.MIN_PRIORITY)

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
