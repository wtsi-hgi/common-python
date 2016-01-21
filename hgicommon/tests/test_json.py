import json
import unittest
from json import JSONEncoder

from hgicommon.tests._stubs import StubModel

from hgicommon.json import get_json_encoders_for_type, register_json_encoder, RegisteredTypeJSONEncoder, \
    reset_registered_json_encoders, _json_encoders


class TestMethodsInJson(unittest.TestCase):
    """
    Tests for `get_json_encoders_for_type`, `register_json_encoder` and `reset_registered_json_encoders`.
    """
    def test_none_if_not_known(self):
        self.assertIsNone(get_json_encoders_for_type(JSONEncoder))

    def test_has_encoders_for_standard_types(self):
        repeat_to_test_reset = True
        while repeat_to_test_reset:
            self.assertTrue(issubclass(get_json_encoders_for_type(dict), JSONEncoder))
            self.assertTrue(issubclass(get_json_encoders_for_type(list), JSONEncoder))
            self.assertTrue(issubclass(get_json_encoders_for_type(tuple), JSONEncoder))
            self.assertTrue(issubclass(get_json_encoders_for_type(str), JSONEncoder))
            self.assertTrue(issubclass(get_json_encoders_for_type(int), JSONEncoder))
            self.assertTrue(issubclass(get_json_encoders_for_type(float), JSONEncoder))
            self.assertTrue(issubclass(get_json_encoders_for_type(bool), JSONEncoder))
            self.assertTrue(issubclass(get_json_encoders_for_type(type(None)), JSONEncoder))
            reset_registered_json_encoders()
            repeat_to_test_reset = False

    def test_can_get_if_registered(self):
        register_json_encoder(JSONEncoder, JSONEncoder)
        self.assertEqual(get_json_encoders_for_type(JSONEncoder), JSONEncoder)

    def test_can_reset(self):
        register_json_encoder(JSONEncoder, JSONEncoder)
        reset_registered_json_encoders()
        self.assertIsNone(get_json_encoders_for_type(JSONEncoder))

    def tearDown(self):
        reset_registered_json_encoders()


class TestRegisteredTypeJSONEncoder(unittest.TestCase):
    """
    Tests for `RegisteredTypeJSONEncoder`.
    """
    def test_default_when_unknown(self):
        self.assertRaises(TypeError, json.dumps, StubModel(), cls=RegisteredTypeJSONEncoder)

    def test_default_when_standard_type(self):
        dict = {1: 2, 3: []}
        self.assertEqual(json.dumps(dict, cls=RegisteredTypeJSONEncoder), json.dumps(dict))

    def test_default_when_registered_type(self):
        custom = StubModel()
        expect_encode = "custom encode"

        class StubModelJSONEncoder(JSONEncoder):
            def default(self, o):
                assert isinstance(o, StubModel)
                return expect_encode
        register_json_encoder(StubModel, StubModelJSONEncoder)

        self.assertEqual(json.dumps(custom, cls=RegisteredTypeJSONEncoder), json.dumps(expect_encode))

    def tearDown(self):
        reset_registered_json_encoders()
