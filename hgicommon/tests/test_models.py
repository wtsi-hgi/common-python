import unittest
from datetime import date

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
    class _MockPriorty(Priority):
        pass

    def setUp(self):
        self.priority_model_1 = TestPriority._MockPriorty(Priority.MIN_PRIORITY)
        self.priority_model_2 = TestPriority._MockPriorty(Priority.MAX_PRIORITY - 1)
        self.priority_model_3 = TestPriority._MockPriorty(Priority.MAX_PRIORITY)

    def test_less_than(self):
        self.assertLess(self.priority_model_1, self.priority_model_2)
        self.assertLess(self.priority_model_1, self.priority_model_3)

    def test_less_than_or_equal(self):
        self.assertLessEqual(self.priority_model_2, self.priority_model_2)
        self.assertLessEqual(self.priority_model_2, self.priority_model_3)

    def test_equal(self):
        self.assertEquals(self.priority_model_1, self.priority_model_1)

    def test_not_equal(self):
        self.assertNotEqual(self.priority_model_1, self.priority_model_2)
        self.assertNotEqual(self.priority_model_1, self.priority_model_3)
        self.assertNotEqual(self.priority_model_2, self.priority_model_3)

    def test_greater_than_or_equal(self):
        self.assertGreaterEqual(self.priority_model_3, self.priority_model_2)
        self.assertGreaterEqual(self.priority_model_3, self.priority_model_3)

    def test_greater_than(self):
        self.assertGreater(self.priority_model_3, self.priority_model_2)
        self.assertGreater(self.priority_model_3, self.priority_model_1)


if __name__ == "__main__":
    unittest.main()
