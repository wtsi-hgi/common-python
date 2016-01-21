from json import JSONEncoder

from hgicommon.collections import Metadata
from hgicommon.json import DefaultSupportedReturnType
from hgicommon.models import Model


class ModelJSONEncoder(JSONEncoder):
    """
    JSON encoder for `Model` instances.
    """
    def default(self, to_encode: Model) -> DefaultSupportedReturnType:
        model_as_dict = dict()
        for property_name, value in vars(to_encode).items():
            model_as_dict[property_name] = value
        return model_as_dict


class MetadataJSONEncoder(JSONEncoder):
    """
    JSON encoder for `Metadata` instances.
    """
    def default(self, to_encode: Metadata) -> DefaultSupportedReturnType:
        return to_encode._data
