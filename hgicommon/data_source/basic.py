import copy
from typing import List
from typing import Sequence, Iterable

from hgicommon.data_source.common import DataSource
from hgicommon.data_source.common import DataSourceType


class MultiDataSource(DataSource[DataSourceType]):
    """
    Aggregator of instances of data from multiple sources.
    """
    def __init__(self, sources: Iterable[DataSource]=()):
        """
        Constructor.
        :param sources: the sources of instances of `DataSourceType`
        """
        self.sources = copy.copy(sources)

    def get_all(self) -> Sequence[DataSourceType]:
        aggregated = []
        for source in self.sources:
            aggregated.extend(source.get_all())
        return aggregated


class ListDataSource(DataSource[DataSourceType]):
    """
    Data source where data is stored in a (changeable) list.
    """
    def __init__(self, data: List[DataSourceType]=None):
        if data is None:
            data = []
        self.data = data

    def get_all(self) -> Sequence[DataSourceType]:
        return self.data
