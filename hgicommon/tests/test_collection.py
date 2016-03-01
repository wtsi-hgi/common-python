import copy
import unittest

from hgicommon.collections import Metadata


class TestMetadata(unittest.TestCase):
    """
    Tests for `Metadata`.
    """
    _TEST_VALUES = {1: 2, 3: 4}

    def setUp(self):
        self.metadata = Metadata(TestMetadata._TEST_VALUES)

    def test_init_with_no_values(self):
        self.assertEqual(len(Metadata()), 0)

    def test_init_with_values(self):
        self.assertCountEqual(self.metadata.keys(), TestMetadata._TEST_VALUES.keys())
        self.assertCountEqual(self.metadata.values(), TestMetadata._TEST_VALUES.values())

    def test_get(self):
        self.assertEqual(self.metadata.get(1), TestMetadata._TEST_VALUES[1])
        self.assertEqual(self.metadata[1], TestMetadata._TEST_VALUES[1])

    def test_rename(self):
        self.metadata.rename(1, 10)
        self.assertNotIn(1, self.metadata)
        self.assertEqual(self.metadata[10], 2)

    def test_rename_non_existent(self):
        self.assertRaises(KeyError, self.metadata.rename, 10, 20)

    def test_rename_to_same_name(self):
        self.metadata.rename(1, 1)
        self.assertEqual(self.metadata[1], 2)

    def test_pop(self):
        self.metadata.pop(1)
        self.assertEqual(self.metadata, Metadata({3: 4}))

    def test_clear(self):
        self.metadata.clear()
        self.assertEqual(self.metadata, Metadata())

    def test_delete(self):
        del self.metadata[1]
        self.assertEqual(self.metadata, Metadata({3: 4}))

    def test_len(self):
        self.assertEqual(len(self.metadata), 2)

    def test_items(self):
        self.assertCountEqual(self.metadata.items(), [(1, 2), (3, 4)])

    def test_values(self):
        self.assertCountEqual(self.metadata.values(), [2, 4])

    def test_keys(self):
        self.assertCountEqual(self.metadata.keys(), [1, 3])

    def test_eq_when_equal(self):
        self.assertEqual(Metadata(TestMetadata._TEST_VALUES), Metadata(TestMetadata._TEST_VALUES))

    def test_eq_when_not_eqal(self):
        self.assertNotEqual(Metadata(TestMetadata._TEST_VALUES), Metadata())

    def test_repr(self):
        string_representation = repr(self.metadata)
        self.assertTrue(isinstance(string_representation, str))

    def test_contains(self):
        self.assertIn(1, self.metadata)
        self.assertNotIn("a", self.metadata)

    def test_copy(self):
        self.assertEqual(copy.copy(self.metadata), self.metadata)

    def test_deepcopy(self):
        self.assertEqual(copy.deepcopy(self.metadata), self.metadata)

if __name__ == "__main__":
    unittest.main()
