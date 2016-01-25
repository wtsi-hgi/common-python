from hgicommon.models import Model


class JSONMapping(Model):
    """
    Model of a mapping between a json property and a property of an object
    """
    def __init__(
            self, json_property: str, object_property: str, constructor_argument: str=None):
        self.json_property = json_property
        self.object_property = object_property
        self.constructor_argument = constructor_argument
