import copy
from abc import abstractmethod, ABCMeta
from typing import List
from typing import Sequence, Iterable, TypeVar, Generic

from hgicommon.data_source.common import DataSource
from hgicommon.data_source.common import SourceDataType


class MultiDataSource(DataSource[SourceDataType]):
    """
    Aggregator of instances of data from multiple sources.
    """
    def __init__(self, sources: Iterable[DataSource]=()):
        """
        Constructor.
        :param sources: the sources of instances of `SourceDataType`
        """
        self.sources = copy.copy(sources)

    def get_all(self) -> Sequence[SourceDataType]:
        aggregated = []
        for source in self.sources:
            aggregated.extend(source.get_all())
        return aggregated


class ListDataSource(DataSource[SourceDataType]):
    """
    Data source where data is stored in a (changeable) list.
    """
    def __init__(self, data: List[SourceDataType]=None):
        if data is None:
            data = []
        self.data = data

    def get_all(self) -> Sequence[SourceDataType]:
        return self.data
