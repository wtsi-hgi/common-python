from typing import Iterable

from hgicommon.data_source.common import DataSourceType
from hgicommon.data_source.dynamic_from_file import RegisteringDataSource
from hgicommon.data_source.static_from_file import FilesDataSource, SynchronisedFilesDataSource
from hgicommon.models import Model


class StubModel(Model):
    """
    Stub `Model`.
    """
    def __init__(self):
        super(Model, self).__init__()


class StubFilesDataSource(FilesDataSource):
    """
    Stub `FilesDataSource`.
    """
    def is_data_file(self, file_path: str) -> bool:
        pass

    def extract_data_from_file(self, file_path: str) -> Iterable[DataSourceType]:
        pass


class StubSynchronisedInFileDataSource(SynchronisedFilesDataSource):
    """
    Stub `SynchronisedFilesDataSource`.
    """
    def is_data_file(self, file_path: str) -> bool:
        pass

    def extract_data_from_file(self, file_path: str) -> Iterable[DataSourceType]:
        pass


class StubRegisteringDataSource(RegisteringDataSource):
    """
    Stub implementation of `RegisteringDataSource`.
    """
    def is_data_file(self, file_path: str) -> bool:
        pass
