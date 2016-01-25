import unittest

from hgicommon.collections import Metadata
from hgicommon.models import Model
from hgicommon.serialisation.json.builders import MappingJSONEncoderClassBuilder
from hgicommon.serialisation.json.encoders import MetadataJSONEncoder
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
        self.encoding_cls = _Example
        self.mapping = _EXAMPLE_JSON_MAPPINGS

        encoder_builder = MappingJSONEncoderClassBuilder()
        encoder_builder.encoding_cls = self.encoding_cls
        encoder_builder.mappings = self.mapping
        self.encoder_cls = encoder_builder.build()

    def test_default(self):
        example_object = _Example(2)
        encoded = self.encoder_cls().default(example_object)
        self.assertDictEqual(encoded, {"json_a": 1, "json_b": 2})


class TestMetadataJSONEncoder(unittest.TestCase):
    """
    Tests for `MetadataJSONEncoder`.
    """
    def setUp(self):
        self.encoder = MetadataJSONEncoder()

    def test_default(self):
        metadata_as_dict = {
            1: 2,
            3: 4
        }
        metadata = Metadata(metadata_as_dict)
        encoded = self.encoder.default(metadata)
        self.assertDictEqual(encoded, metadata_as_dict)


if __name__ == "__main__":
    unittest.main()
