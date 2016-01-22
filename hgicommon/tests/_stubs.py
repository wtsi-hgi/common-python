from json import JSONEncoder

from hgicommon.json import _RegisteredTypeJSONEncoder

from hgicommon.models import Model


class StubModel(Model):
    """
    Stub `Model`.
    """
    pass


class StubRegisteredTypeJSONEncoder(_RegisteredTypeJSONEncoder):
    """
    Stub `_RegisteredTypeJSONEncoder`.
    """
    def _get_json_encoders_for_type(self) -> JSONEncoder:
        pass
