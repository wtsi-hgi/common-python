import copy
import os
import unittest
from tempfile import mkdtemp
from typing import Any
from unittest.mock import MagicMock

import shutil

from hgicommon.data_source import StaticDataSource, MultiDataSource
from hgicommon.tests._helpers import write_data_to_files_in_temp_directory, extract_data_from_file
from hgicommon.tests._stubs import StubInFileDataSource


class TestMultiSource(unittest.TestCase):
    """
    Tests for `MultiDataSource`.
    """
    def setUp(self):
        self.data = [i for i in range(10)]
        self.sources = [StaticDataSource([self.data[i]]) for i in range(len(self.data))]

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


class TestStaticDataSource(unittest.TestCase):
    """
    Tests for `StaticDataSource`.
    """
    def setUp(self):
        self.data = [i for i in range(10)]

    def test_init_change_of_source_list_has_no_effect(self):
        data = copy.copy(self.data)
        source = StaticDataSource(data)
        data.pop()
        self.assertCountEqual(source.get_all(), self.data)

    def test_get_all(self):
        source = StaticDataSource(self.data)
        self.assertCountEqual(source.get_all(), self.data)


class TestInFileDataSource(unittest.TestCase):
    """
    Tests for `InFileDataSource`.
    """
    def setUp(self):
        self.maxDiff = None

        self.data = [i for i in range(30)]
        self.temp_directory = write_data_to_files_in_temp_directory(self.data, 10)

        def extract_adapter(file_path: str) -> Any:
            return extract_data_from_file(file_path, parser=lambda data: int(data), separator='\n')

        self.source = StubInFileDataSource(self.temp_directory)
        self.source.is_data_file = MagicMock(return_value=True)
        self.source.extract_data_from_file = MagicMock(side_effect=extract_adapter)

    def test_get_all_with_empty_directory(self):
        empty_directory = mkdtemp(suffix=self._testMethodName)
        source = StubInFileDataSource(empty_directory)

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
        pass



class TestSynchronisedInFileDataSource(unittest.TestCase):
    """
    Tests for `SynchronisedInFileDataSource`.
    """
    pass


if __name__ == "__main__":
    unittest.main()
