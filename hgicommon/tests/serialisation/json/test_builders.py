import unittest

from hgicommon.serialisation.json.builders import MappingJSONEncoderClassBuilder, MappingJSONDecoderClassBuilder
from hgicommon.serialisation.json.models import JSONMapping
from hgicommon.tests._stubs import StubModel


JSON_MAPPINGS = [
    JSONMapping("json_a", "a"),
    JSONMapping("json_b", "b")
]


class TestMappingJSONEncoderClassBuilder(unittest.TestCase):
    """
    Tests for `MappingJSONEncoderClassBuilder`.
    """
    def test_build(self):
        cls = StubModel

        encoder_builder = MappingJSONEncoderClassBuilder()
        encoder_builder.encoding_cls = cls
        encoder_builder.mappings = JSON_MAPPINGS

        encoder = encoder_builder.build()

        self.assertEqual(encoder.ENCODING_CLS, cls)
        self.assertEqual(encoder.JSON_MAPPINGS, JSON_MAPPINGS)


class TestMappingJSONDecoderClassBuilder(unittest.TestCase):
    """
    Tests for `MappingJSONDecoderClassBuilder`.
    """
    def test_build(self):
        cls = StubModel

        decoder_builder = MappingJSONDecoderClassBuilder()
        decoder_builder.encoding_cls = cls
        decoder_builder.mappings = JSON_MAPPINGS

        decoder = decoder_builder.build()

        self.assertEqual(decoder.DECODING_CLS, cls)
        self.assertEqual(decoder.JSON_MAPPINGS, JSON_MAPPINGS)


if __name__ == "__main__":
    unittest.main()
