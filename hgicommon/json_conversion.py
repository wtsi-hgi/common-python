from json import JSONEncoder
from typing import Dict, Any

from hgicommon.collections import Metadata
from hgicommon.json import DefaultSupportedReturnType


class ObjectJSONEncoder(JSONEncoder):
    """
    JSON encoder for `object` instances (those that just define properties, such as subclasses of `Model`).

    Do not use as cls in `json.dumps` if the object being serialised has properties with types that cannot be converted
    to JSON by default. In such cases, this class can be used in `JSONEncoderClassBuilder` along with encoders that
    handle other unsupported types.
    """
    def default(self, to_encode: object) -> DefaultSupportedReturnType:
        assert isinstance(to_encode, object)

        model_as_dict = dict()  # type: Dict[str, Any]
        for property_name, value in vars(to_encode).items():
            model_as_dict[property_name] = value

        return model_as_dict


# `Model` JSON encoder, defined for completeness
ModelJSONEncoder = ObjectJSONEncoder


class MetadataJSONEncoder(JSONEncoder):
    """
    JSON encoder for `Metadata` instances.

    Do not use as cls in `json.dumps` if the metadata collection being serialised contains values with types that cannot
    be converted to JSON by default. In such cases, this class can be used in `JSONEncoderClassBuilder` along with
    encoders that handle other unsupported types.
    """
    def default(self, to_encode: Metadata) -> DefaultSupportedReturnType:
        if not isinstance(to_encode, Metadata):
            super().default(to_encode)

        return to_encode._data
