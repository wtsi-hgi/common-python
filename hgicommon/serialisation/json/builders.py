from typing import Iterable, TypeVar

from hgicommon.serialisation.json.decoders import _MappingJSONDecoder
from hgicommon.serialisation.json.encoders import _MappingJSONEncoder
from hgicommon.serialisation.json.models import JSONMapping


# Type of a concrete subclass of `_MappingJSONEncoder`, created dynamically.
MappingJSONEncoderType = TypeVar("MappingJSONEncoder", bound=_MappingJSONEncoder)

# Type of a concrete subclass of `_MappingJSONDecoder`, created dynamically.
MappingJSONDecoderType = TypeVar("MappingJSONDecoder", bound=_MappingJSONDecoder)


class MappingJSONEncoderClassBuilder:
    """
    Builder for `_MappingJSONEncoder` concrete subclasses.
    """
    def __init__(self):
        """
        Constructor.
        """
        self.encoding_cls = type(None)    # type: type
        self.mappings = []  # type: Iterable[JSONMapping]

    def build(self) -> MappingJSONEncoderType:
        """
        Build a subclass of `_MappingJSONEncoder`.
        :return: the built subclass
        """
        class_name = "%sJSONEncoder" % self.encoding_cls.__name__
        return type(
            class_name,
            (_MappingJSONEncoder, ),
            {
                "ENCODING_CLS": self.encoding_cls,
                "JSON_MAPPINGS": self.mappings
            }
        )


class MappingJSONDecoderClassBuilder:
    """
    Builder for `_MappingJSONDecoder` concrete subclasses.
    """
    def __init__(self):
        """
        Constructor.
        """
        self.encoding_cls = type(None)    # type: type
        self.mappings = []  # type: Iterable[JSONMapping]

    def build(self) -> MappingJSONDecoderType:
        """
        Build a subclass of `_MappingJSONDecoder`.
        :return: the built subclass
        """
        class_name = "%sJSONDecoder" % self.encoding_cls.__name__
        return type(
            class_name,
            (_MappingJSONDecoder, ),
            {
                "DECODING_CLS": self.encoding_cls,
                "JSON_MAPPINGS": self.mappings
            }
        )
