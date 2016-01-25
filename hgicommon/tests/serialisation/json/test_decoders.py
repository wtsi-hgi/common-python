import json
import unittest

from hgicommon.models import Model

from hgicommon.serialisation.json.builders import MappingJSONDecoderClassBuilder
from hgicommon.serialisation.json.models import JSONMapping


class _Example(Model):
    def __init__(self, c):
        self.a = 1
        self.b = c

_EXAMPLE_JSON_MAPPINGS = [
    JSONMapping("json_a", "a"),
    JSONMapping("json_b", "b", constructor_argument="c")
]


class TestMappingJSONEncoder(unittest.TestCase):
    """
    Tests for `_MappingJSONEncoder`.
    """
    def setUp(self):
        self.decoding_cls = _Example
        self.mapping = _EXAMPLE_JSON_MAPPINGS

        decoder_builder = MappingJSONDecoderClassBuilder()
        decoder_builder.encoding_cls = self.decoding_cls
        decoder_builder.mappings = self.mapping
        self.decoder_cls = decoder_builder.build()

    def test_decode(self):
        example_as_dict = {"json_a": 1, "json_b": 2}
        example_as_string = json.dumps(example_as_dict)

        decoded = self.decoder_cls().decode(example_as_string)
        self.assertIsInstance(decoded, _Example)
        self.assertEqual(decoded.a, 1)
        print(decoded)
        self.assertEqual(decoded.b, 2)


if __name__ == "__main__":
    unittest.main()
