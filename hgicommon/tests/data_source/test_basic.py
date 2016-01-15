import unittest

from hgicommon.data_source import ListDataSource, MultiDataSource


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
        self.assertEqual(len(source.get_all()), 0)

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

    def test_init_data_optional(self):
        source = ListDataSource()
        for datum in self.data:
            source.data.append(datum)
        self.assertCountEqual(source.get_all(), self.data)

    def test_init_data_can_be_changed(self):
        source = ListDataSource(self.data)
        self.data.append(11)
        self.assertCountEqual(source.get_all(), self.data)

    def test_get_all(self):
        source = ListDataSource(self.data)
        self.assertCountEqual(source.get_all(), self.data)


if __name__ == "__main__":
    unittest.main()
