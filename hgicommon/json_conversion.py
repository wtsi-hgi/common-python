import json
from json import JSONEncoder

from hgicommon.models import Model


class ModelJSONEncoder(JSONEncoder):
    """
    Model JSON encoder.
    """
    def default(self, to_encode: Model):
        # if not isinstance(to_encode, Model):
        #     raise TypeError("`ModelJSONEncoder` can only JSON encode objects that inherit from `Model`: `%s` given"
        #                     % type(to_encode))

        model_as_dict = dict()
        for property_name, value in vars(to_encode).items():
            model_as_dict[property_name] = value
        return model_as_dict