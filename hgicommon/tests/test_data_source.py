import copy
import unittest
from tempfile import mkdtemp, mkstemp
from hgicommon.data_source import StaticDataSource, MultiDataSource


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
        self.temp_directory = mkdtemp(self._testMethodName)
        self.data = [i for i in range(12)]

        mkstemp(dir=self.temp_directory, text=self.data[0:3])

        # TODO



class TestSynchronisedInFileDataSource(unittest.TestCase):
    """
    Tests for `SynchronisedInFileDataSource`.
    """
    pass


if __name__ == "__main__":
    unittest.main()
