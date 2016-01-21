import copy
from json import JSONEncoder
from typing import Tuple, Dict, Union, List, Optional, Iterable, Any

# Return type of JSONEncoder.default
DefaultSupportedReturnType = Union[
    Dict, List, Tuple, str, int, float, bool, None
]

# Encoders for objects that are handled by the in-build JSON library
_DEFAULT_JSON_ENCODERS = {
    dict: JSONEncoder,
    list: JSONEncoder,
    tuple: JSONEncoder,
    str: JSONEncoder,
    int: JSONEncoder,
    float: JSONEncoder,
    bool: JSONEncoder,
    type(None): JSONEncoder
}

# Registered JSON encoders
_json_encoders = copy.copy(_DEFAULT_JSON_ENCODERS)


def get_json_encoders_for_type(type_to_encode: type) -> Optional[Iterable[JSONEncoder]]:
    """
    Gets the registered JSON encoder for the given type.
    :param type_to_encode: the type of object that is to be encoded
    :return: the encoder for the given object else `None` if unknown
    """
    global _json_encoders
    if type_to_encode not in _json_encoders:
        return None
    return _json_encoders[type_to_encode]


def register_json_encoder(encoder_type: type, encoder: JSONEncoder):
    """
    Register the given JSON encoder for use with the given object type.

    Warning: use this method carefully - it affects global scope!
    :param encoder_type: the type of object to encode
    :param encoder: the JSON encoder
    """
    global _json_encoders
    _json_encoders[encoder_type] = encoder


def reset_registered_json_encoders():
    """
    Resets registered JSON encoders so that only ones supported by the in-built library are supported.

    Warning: use this method carefully - it affects global scope!
    """
    global _json_encoders
    _json_encoders = copy.copy(_DEFAULT_JSON_ENCODERS)


class RegisteredTypeJSONEncoder(JSONEncoder):
    """
    JSON encoder that will encode objects using the registered encoders. Works with in-built JSON library:
    ```
    import json

    register_json_encoder(MyObjectType, MyEncoderType)
    json.dumps(object_to_serialise, cls=RegisteredTypeJSONEncoder)
    ```
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._args = args
        self._kwargs = kwargs

    def default(self, to_encode: Any) -> DefaultSupportedReturnType:
        type_to_encode = type(to_encode)

        encoder_type = get_json_encoders_for_type(type_to_encode)
        if encoder_type is None:
            # Unknown type: let standard JSON parser deal with it (will almost certainly raise an exception)
            encoder_type = JSONEncoder
        assert isinstance(encoder_type, type)

        encoder = encoder_type(*self._args, **self._kwargs)
        assert isinstance(encoder, JSONEncoder)

        return encoder.default(to_encode)
