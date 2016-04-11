import copy
import unittest
from datetime import date

from hgicommon.tests._stubs import StubModel


class TestModel(unittest.TestCase):
    """
    Test cases for `Model`.
    """
    def setUp(self):
        self._model = StubModel()
        self._model.property_1 = 1
        self._model.property_2 = "a"
        self._model.property_3 = [i for i in range(1000)]
        self._model.property_4 = set([i for i in range(1000)])
        print(self._model)

    def test_equal_non_nullity(self):
        self.assertNotEqual(self._model, None)

    def test_equal_different_type(self):
        self.assertNotEqual(self._model, date)

    def test_equal_reflexivity(self):
        model = self._model
        self.assertEqual(model, model)

    def test_equal_symmetry(self):
        model1 = self._model
        model2 = copy.copy(self._model)
        self.assertEqual(model1, model2)
        self.assertEqual(model2, model1)

    def test_equal_transitivity(self):
        model1 = self._model
        model2 = copy.copy(self._model)
        model3 = copy.copy(self._model)
        self.assertEqual(model1, model2)
        self.assertEqual(model2, model3)
        self.assertEqual(model1, model3)

    def test_can_get_string_representation(self):
        string_representation = str(self._model)
        self.assertTrue(isinstance(string_representation, str))

    def test_can_get_representation(self):
        string_representation = repr(self._model)
        self.assertTrue(isinstance(string_representation, str))


if __name__ == "__main__":
    unittest.main()
