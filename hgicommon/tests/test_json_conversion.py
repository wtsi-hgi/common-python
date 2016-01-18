import json
import unittest

from hgicommon.json_conversion import ModelJSONEncoder
from hgicommon.tests._stubs import StubModel


class TestModelJSONEncoder(unittest.TestCase):
    """
    Tests for `ModelJSONEncoder`.
    """
    def setUp(self):
        self._model = StubModel()
        self._model.property_1 = 1
        self._model.property_2 = "a"
        self._model.property_3 = []

    def test_with_empty_model(self):
        serialised = json.dumps(StubModel(), cls=ModelJSONEncoder)
        self.assertEqual(serialised, json.dumps({}))

    def test_with_model(self):
        serialised = json.dumps(self._model, cls=ModelJSONEncoder)
        self.assertEqual(serialised, json.dumps({"property_1": 1, "property_2": "a", "property_3": []}))

    def test_with_nested_model(self):
        nested = [{"test": self._model}]
        serialised = json.dumps(nested, cls=ModelJSONEncoder)
        self.assertEqual(serialised, json.dumps([{"test": {"property_1": 1, "property_2": "a", "property_3": []}}]))



if __name__ == "__main__":
    unittest.main()
