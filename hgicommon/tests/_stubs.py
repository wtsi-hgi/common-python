from typing import Iterable

from hgicommon.data_source import InFileDataSource, SourceDataType
from hgicommon.models import Model


class StubModel(Model):
    """
    Stub `Model`.
    """
    def __init__(self):
        super(Model, self).__init__()


class StubInFileDataSource(InFileDataSource):
    """
    Stub `InFileDataSource`.
    """
    def is_data_file(self, file_path: str) -> bool:
        pass

    def extract_data_from_file(self, file_path: str) -> Iterable[SourceDataType]:
        pass