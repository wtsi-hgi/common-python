from abc import ABCMeta,abstractmethod
from typing import Generic, Sequence, TypeVar

DataSourceType = TypeVar("T")


class DataSource(Generic[DataSourceType]):
    """
    A source of instances of `DataSourceType`.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all(self) -> Sequence[DataSourceType]:
        """
        Gets the data at the source.
        :return: instances of `DataSourceType`
        """
        pass

