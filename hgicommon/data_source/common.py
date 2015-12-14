from abc import ABCMeta,abstractmethod
from typing import Generic, Sequence, TypeVar

SourceDataType = TypeVar('T')


class DataSource(Generic[SourceDataType]):
    """
    A source of instances of `SourceDataType`.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all(self) -> Sequence[SourceDataType]:
        """
        Gets the data aty the source
        :return: instances of `SourceDataType`
        """
        pass

