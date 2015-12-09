import collections
import copy
import glob
from abc import abstractmethod
from threading import Thread
from typing import Dict
from typing import Sequence, Iterable, TypeVar, Generic

from multiprocessing import Lock

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

SourceDataType = TypeVar('T')


# XXX: Making this abstract for some reason interferes with generics
class DataSource(Generic[SourceDataType]):
    """
    A source of instances of `SourceDataType`.
    """
    @abstractmethod
    def get_all(self) -> Sequence[SourceDataType]:
        """
        Gets the data aty the source
        :return: instances of `SourceDataType`
        """
        pass


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


class StaticDataSource(DataSource[SourceDataType]):
    """
    Static source of data.
    """
    def __init__(self, data: Iterable[SourceDataType]):
        if not isinstance(data, collections.Iterable):
            raise ValueError("Data must be iterable")
        self._data = copy.copy(data)

    def get_all(self) -> Sequence[SourceDataType]:
        return self._data


class InFileDataSource(DataSource[SourceDataType]):
    """
    TODO
    """
    def __init__(self, directory_location: str):
        """
        Default constructor.
        :param directory_location: the location of the processor
        """
        self._directory_location = directory_location
        self._observer = None
        self._file_locations = dict()   # type: Dict[str, SourceDataType]
        self._load_all_in_directory()

    @abstractmethod
    def _extract_data_from_file(self, file_path: str) -> Iterable[SourceDataType]:
        """
        Extracts data from the file at the given file path.
        :param file_path: the path to the file to extract data from
        :return: the extracted data
        """
        pass

    @abstractmethod
    def _is_data_file(self, file_path: str) -> bool:
        """
        Determines whether the file at the given path is of interest.
        :param file_path: path to the updated file
        :return: whether the file is of interest
        """
        pass

    def get_all(self) -> Sequence[SourceDataType]:
        data = []
        for key, values in self._file_locations.items():
            data.extend(values)
        return data

    def _load_all_in_directory(self):
        """
        TODO
        """
        for file_path in glob.iglob("%s/**/*" % self._directory_location, recursive=True):
            if self._is_data_file(file_path):
                self._file_locations[file_path] = self._extract_data_from_file(file_path)


class SynchronisedInFileDataSource(InFileDataSource):
    """
    TODO
    """
    def __init__(self, directory_location: str):
        """
        Default constructor.
        :param directory_location:
        :return:
        """
        super().__init__(directory_location)
        self._status_lock = Lock()
        self._running = False

        self._event_handler = FileSystemEventHandler()
        self._event_handler.on_created = self._on_file_created
        self._event_handler.on_modified = self._on_file_modified
        self._event_handler.on_deleted = self._on_file_deleted

    def start(self):
        """
        Monitors data kept in files in the predefined directory in a new thread.
        """
        self._status_lock.acquire()
        if self._running:
            raise RuntimeError("Already running")
        self._running = True

        self._observer = Observer()
        self._observer.schedule(self._event_handler, self._directory_location, recursive=True)
        self._observer.start()
        self._status_lock.release()

    def stop(self):
        """
        Stops monitoring the predefined directory.
        """
        self._status_lock.acquire()
        if self._running:
            assert self._observer is not None
            self._observer.stop()
            self._observer = None
            self._running = False
        self._status_lock.release()

    def _on_file_created(self, event: FileSystemEvent):
        """
        Called when a file in the monitored directory has been created.
        :param event: the file system event
        """
        # TODO: If a directory is created, are events generated for just the directory or all of the files in the
        # directory?
        if not event.is_directory and InFileDataSource._is_data_file(event.src_path):
            assert event.src_path not in self._file_locations
            self._file_locations[event.src_path] = self._extract_data_from_file(event.src_path)

    def _on_file_modified(self, event: FileSystemEvent):
        """
        Called when a file in the monitored directory has been modified.
        :param event: the file system event
        """
        # TODO: If a directory is modified, are events generated for just the directory or all of the files in the
        # directory?
        if not event.is_directory and InFileDataSource._is_data_file(event.src_path):
            assert event.src_path in self._file_locations
            self._file_locations[event.src_path] = self._extract_data_from_file(event.src_path)

    def _on_file_deleted(self, event: FileSystemEvent):
        """
        Called when a file in the monitored directory has been deleted.
        :param event: the file system event
        """
        # TODO: If a directory is deleted, are events generated for just the directory or all of the files in the
        # directory?
        if not event.is_directory and InFileDataSource._is_data_file(event.src_path):
            assert event.src_path in self._file_locations
            del(self._file_locations[event.src_path])

