import json
import unittest

from hgicommon.json_conversion import ObjectJSONEncoder
from hgicommon.tests._stubs import StubModel


class TestModelJSONEncoder(unittest.TestCase):
    """
    Tests for `ObjectJSONEncoder`.
    """
    def setUp(self):
        self._model = StubModel()
        self._model.property_1 = {1: 2}
        self._model.property_2 = ["a"]
        self._model_serialised = {"property_1": {1: 2}, "property_2": ["a"]}

    def test_with_empty_model(self):
        serialised = json.dumps(StubModel(), cls=ObjectJSONEncoder)
        self.assertEqual(serialised, json.dumps({}))

    def test_with_model(self):
        serialised = json.dumps(self._model, cls=ObjectJSONEncoder)
        self.assertEqual(serialised, json.dumps(self._model_serialised))

    def test_with_nested_model(self):
        inner_model = StubModel()
        inner_model.property_1 = 1
        self._model.property_3 = inner_model
        self._model_serialised["property_3"] = {"property_1": 1}

        serialised = json.dumps(self._model, cls=ObjectJSONEncoder)
        self.assertEqual(serialised, json.dumps(self._model_serialised))


if __name__ == "__main__":
    unittest.main()
