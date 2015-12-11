import copy
import glob
import logging
import os
import shutil
import unittest
from multiprocessing import Lock
from tempfile import mkdtemp
from threading import Semaphore
from time import sleep
from typing import Any, List, Tuple
from unittest.mock import MagicMock

from watchdog.events import FileSystemEventHandler

from hgicommon.data_source import ListDataSource, MultiDataSource, FileSystemChange
from hgicommon.tests._helpers import write_data_to_files_in_temp_directory, extract_data_from_file
from hgicommon.tests._stubs import StubFilesDataSource, StubSynchronisedInFileDataSource


class TestMultiDataSource(unittest.TestCase):
    """
    Tests for `MultiDataSource`.
    """
    def setUp(self):
        self.data = [i for i in range(10)]
        self.sources = [ListDataSource([self.data[i]]) for i in range(len(self.data))]

    def test_init_change_of_source_list_has_no_effect(self):
        source = MultiDataSource(self.sources)
        self.sources.pop()
        self.assertCountEqual(source.get_all(), self.data)

    def test_get_all_when_no_sources(self):
        source = MultiDataSource()
        self.assertEquals(len(source.get_all()), 0)

    def test_get_all_when_sources(self):
        source = MultiDataSource(self.sources)
        self.assertIsInstance(source.get_all()[0], type(self.data[0]))
        self.assertCountEqual(source.get_all(), self.data)


class TestListDataSource(unittest.TestCase):
    """
    Tests for `ListDataSource`.
    """
    def setUp(self):
        self.data = [i for i in range(10)]

    def test_init_list_can_be_changed(self):
        source = ListDataSource(self.data)
        self.data.append(11)
        self.assertCountEqual(source.get_all(), self.data)

    def test_get_all(self):
        source = ListDataSource(self.data)
        self.assertCountEqual(source.get_all(), self.data)


class TestFilesDataSource(unittest.TestCase):
    """
    Tests for `FilesDataSource`.
    """
    def setUp(self):
        self.maxDiff = None

        self.data = [i for i in range(30)]
        self.temp_directory = write_data_to_files_in_temp_directory(self.data, 10)

        def extract_adapter(file_path: str) -> Any:
            return extract_data_from_file(file_path, parser=lambda data: int(data), separator='\n')

        self.source = StubFilesDataSource(self.temp_directory)
        self.source.is_data_file = MagicMock(return_value=True)
        self.source.extract_data_from_file = MagicMock(side_effect=extract_adapter)

    def test_get_all_with_empty_directory(self):
        empty_directory = mkdtemp(suffix=self._testMethodName)
        source = StubFilesDataSource(empty_directory)

        retrieved_data = source.get_all()
        self.assertEquals(len(retrieved_data), 0)

    def test_get_all(self):
        retrieved_data = self.source.get_all()
        self.assertCountEqual(retrieved_data, self.data)

    def test_get_all_with_filter(self):
        def data_filter(file_path: str) -> bool:
            with open(file_path, 'r') as file:
                return '29' in file.read()

        self.source.is_data_file = MagicMock(side_effect=data_filter)
        retrieved_data = self.source.get_all()
        self.assertCountEqual(retrieved_data, [27, 28, 29])

    def tearDown(self):
        shutil.rmtree(self.temp_directory)


class TestSynchronisedFilesDataSource(unittest.TestCase):
    """
    Tests for `SynchronisedFilesDataSource`.
    """
    _FILE_PREFIX = "test_file"

    def setUp(self):
        self.maxDiff = None

        self.data = [i for i in range(30)]
        self.temp_directory = write_data_to_files_in_temp_directory(
            self.data, 10, file_prefix=TestSynchronisedFilesDataSource._FILE_PREFIX)

        def extract_adapter(file_path: str) -> Any:
            return extract_data_from_file(file_path, parser=lambda data: int(data), separator='\n')

        def is_test_file(file_path: str) -> bool:
            return TestSynchronisedFilesDataSource._FILE_PREFIX in file_path

        self.source = StubSynchronisedInFileDataSource(self.temp_directory)
        self.source.is_data_file = MagicMock(side_effect=is_test_file)
        self.source.extract_data_from_file = MagicMock(side_effect=extract_adapter)

    def test_start_if_started(self):
        self.source.start()
        self.assertRaises(RuntimeError, self.source.start)

    def test_start_after_stop(self):
        self.source.start()
        self.source.stop()
        self.source.start()

    def test_get_all_when_never_started(self):
        self.assertRaises(RuntimeError, self.source.get_all)

    def test_get_all_when_stopped(self):
        self.source.start()
        self.source.stop()
        self.assertRaises(RuntimeError, self.source.get_all)

    def test_get_all_when_changed_on_restart(self):
        self.source.start()
        self.assertCountEqual(self.source.get_all(), self.data)
        self.source.stop()
        for file_path in glob.iglob("%s/*" % self.temp_directory):
            os.remove(file_path)
        self.source.start()
        self.assertEquals(len(self.source.get_all()), 0)

    def test_get_all_when_file_created(self):
        self.source.start()
        self._block_until_source_started()

        change_trigger = Semaphore(0)

        def on_change(change: FileSystemChange):
            if change == FileSystemChange.CREATE:
                change_trigger.release()

        self.source.add_listener(on_change)

        more_data = [i for i in range(50)]
        write_data_to_files_in_temp_directory(more_data, 10, dir=self.temp_directory,
                                              file_prefix=TestSynchronisedFilesDataSource._FILE_PREFIX)
        even_more_data = self._add_more_data_in_nested_directory(10)[1]

        triggers = 0
        while triggers != 20:
            change_trigger.acquire()
            triggers += 1

        logging.debug(self.source._origin_mapped_data)
        self.assertCountEqual(self.source.get_all(), self.data + more_data + even_more_data)

    def test_get_all_when_file_deleted(self):
        self.source.start()
        self._block_until_source_started()

        change_lock = Lock()
        change_lock.acquire()

        def on_change(change: FileSystemChange):
            if change == FileSystemChange.DELETE:
                change_lock.release()

        self.source.add_listener(on_change)

        to_delete_file_path = glob.glob("%s/*" % self.temp_directory)[0]
        deleted_data = extract_data_from_file(to_delete_file_path, parser=lambda data: int(data), separator='\n')
        os.remove(to_delete_file_path)

        change_lock.acquire()

        self.assertCountEqual(self.source.get_all(), [x for x in self.data if x not in deleted_data])

    def test_get_all_when_folder_containing_files_is_deleted(self):
        nested_directory_path = self._add_more_data_in_nested_directory()[0]

        self.source.start()
        self._block_until_source_started()

        change_lock = Lock()
        change_lock.acquire()

        def on_change(change: FileSystemChange):
            if change == FileSystemChange.DELETE:
                change_lock.release()

        self.source.add_listener(on_change)

        shutil.rmtree(nested_directory_path)

        change_lock.acquire()

        self.assertCountEqual(self.source.get_all(), self.data)

    def test_get_all_when_file_modified(self):
        self.source.start()
        self._block_until_source_started()

        change_lock = Lock()
        change_lock.acquire()

        def on_change(change: FileSystemChange):
            if change == FileSystemChange.MODIFY:
                change_lock.release()

        self.source.add_listener(on_change)

        to_modify_file_path = glob.glob("%s/*" % self.temp_directory)[0]
        to_modify = extract_data_from_file(to_modify_file_path, parser=lambda data: int(data), separator='\n')
        modified = to_modify[0: -1]
        with open(to_modify_file_path, 'w') as file:
            file.write('\n'.join([str(x) for x in modified]))

        change_lock.acquire()

        self.assertCountEqual(self.source.get_all(), [x for x in self.data if x not in to_modify] + modified)

    def _block_until_source_started(self):
        """
        Blocks until the source has started to notice changes in the file system (may be a few milliseconds after it has
        been started.
        """
        blocked = True

        def unblock(*args):
            nonlocal blocked
            blocked = False

        event_handler = FileSystemEventHandler()
        event_handler.on_modified = unblock
        self.source._observer.schedule(event_handler, self.temp_directory, recursive=True)

        temp_file_path = os.path.join(self.temp_directory, ".temp")
        i = 0
        while blocked:
            with open(temp_file_path, 'a') as file:
                file.write(str(i))
            sleep(10 / 1000)
            i += 1

        # XXX: Not removing the temp file to avoid the notification.
        # XXX: Not unscheduling as observer does not like it for some reason.

    def _add_more_data_in_nested_directory(self, number_of_extra_files: int=1) -> Tuple[str, List[int]]:
        """
        Adds more data in a directory nested inside the temp directory.
        :param number_of_extra_files: (optional) the number of files to put the new data in inside the nested directory
        :return: a tuple where the first value is the path to the new nested directory and the second is the new data
        """
        nested_directory_path = os.path.join(self.temp_directory, "nested")
        os.makedirs(nested_directory_path)
        more_data = [i for i in range(50)]
        write_data_to_files_in_temp_directory(more_data, number_of_extra_files, dir=nested_directory_path,
                                              file_prefix=TestSynchronisedFilesDataSource._FILE_PREFIX)
        return (nested_directory_path, more_data)

    def tearDown(self):
        self.source.stop()
        shutil.rmtree(self.temp_directory)


if __name__ == "__main__":
    unittest.main()
