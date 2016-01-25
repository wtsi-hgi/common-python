from abc import ABCMeta
from json import JSONDecoder
from typing import Iterable
from typing import TypeVar

from hgicommon.serialisation.json.automatic import DefaultSupportedReturnType
from hgicommon.serialisation.json.models import JSONMapping


class _MappingJSONDecoder(JSONDecoder, metaclass=ABCMeta):
    """
    JSON decoder that deserialises an object from JSON based on a mapping.

    As `json.dumps` requires a type rather than an instance and there is no control given over the instatiation, the
    decoded class and the mappings between the object properties and the json properties cannot be passed through the
    constructor. Instead this class must be subclassed and the subclass must define the relevant constants.
    """
    _PLACEHOLDER = TypeVar("")

    DECODING_CLS = _PLACEHOLDER     # type: type
    JSON_MAPPINGS = _PLACEHOLDER    # type: Iterable[JSONMapping]

    def decode(self, json_as_string: str, **kwargs) -> DefaultSupportedReturnType:
        json_as_dict = super().decode(json_as_string)

        init_kwargs = dict()    # Dict[str, Any]
        for mapping in self.JSON_MAPPINGS:
            if mapping.constructor_argument is not None:
                init_kwargs[mapping.constructor_argument] = json_as_dict[mapping.json_property]

        model = self.DECODING_CLS(**init_kwargs)

        for mapping in self.JSON_MAPPINGS:
            if mapping.constructor_argument is None:
                model.__setattr__(mapping.object_property, json_as_dict[mapping.json_property])

        return model
