import unittest

from hgicommon.collections import SearchCriteria, Metadata
from hgicommon.enums import ComparisonOperator
from hgicommon.models import SearchCriterion


class TestSearchCriteria(unittest.TestCase):
    """
    Tests for `SearchCriteria`.
    """
    def setUp(self):
        self._search_criterion1 = SearchCriterion("attribute1", "value1", ComparisonOperator.EQUALS)
        self._search_criterion2 = SearchCriterion("attribute2", "value2", ComparisonOperator.LESS_THAN)

    def test_append_criterion_with_different_attributes(self):
        search_criteria = SearchCriteria()
        search_criteria.append(self._search_criterion1)
        search_criteria.append(self._search_criterion2)
        self.assertCountEqual(search_criteria, [self._search_criterion1, self._search_criterion2])

    def test_append_criterion_with_same_attributes(self):
        search_criteria = SearchCriteria()
        search_criteria.append(self._search_criterion1)
        self.assertRaises(ValueError, search_criteria.append, self._search_criterion1)

    def test_instantiate_with_different_attributes(self):
        search_criteria = SearchCriteria([self._search_criterion1, self._search_criterion2])
        self.assertListEqual(search_criteria, [self._search_criterion1, self._search_criterion2])

    def test_instantiate_with_same_attributes(self):
        self.assertRaises(ValueError, SearchCriteria, [self._search_criterion1, self._search_criterion1])

    def test_extend_with_list_containing_same_value(self):
        search_criteria = SearchCriteria([self._search_criterion1])
        self.assertRaises(ValueError, search_criteria.extend, [self._search_criterion1])

    def test_extend_with_search_criteria(self):
        search_criteria_1 = SearchCriteria([self._search_criterion1])
        search_criteria_2 = SearchCriteria([self._search_criterion2])
        search_criteria_1.extend(search_criteria_2)
        self.assertListEqual(search_criteria_1, [self._search_criterion1, self._search_criterion2])

    def test_set_item(self):
        search_criteria = SearchCriteria([self._search_criterion1])
        search_criteria[0] = self._search_criterion2
        self.assertListEqual(search_criteria, [self._search_criterion2])

    def test_set_item_to_result_in_duplicate(self):
        search_criteria = SearchCriteria([self._search_criterion1, self._search_criterion2])

        def perform_test():
            search_criteria[1] = self._search_criterion1

        self.assertRaises(ValueError, perform_test)

    def test_set_item_replacing_self_with_self(self):
        search_criteria = SearchCriteria([self._search_criterion1, self._search_criterion2])

        def perform_test():
            search_criteria[0] = self._search_criterion1

        self.assertListEqual(search_criteria, [self._search_criterion1, self._search_criterion2])

    def test_create_by_addition_with_duplicates(self):
        search_criteria_1a = SearchCriteria([self._search_criterion1])
        search_criteria_1b = SearchCriteria([self._search_criterion1])

        def perform_test():
            search_criteria_1a + search_criteria_1b

        self.assertRaises(ValueError, perform_test)


class TestMetadata(unittest.TestCase):
    """
    Tests for `Metadata`.
    """
    _TEST_VALUES = {1: 2, 3: 4}

    def test_init_with_initial_values(self):
        metadata = Metadata(TestMetadata._TEST_VALUES)
        self.assertEqual(metadata, TestMetadata._TEST_VALUES)

    def test_set(self):
        metadata = Metadata()
        metadata.set(1, 2)
        metadata[3] = 4
        self.assertEqual(metadata, TestMetadata._TEST_VALUES)

    def test_get(self):
        metadata = Metadata(TestMetadata._TEST_VALUES)
        self.assertEqual(metadata.get(1), TestMetadata._TEST_VALUES[1])
        self.assertEqual(metadata[1], TestMetadata._TEST_VALUES[1])

    def test_rename(self):
        metadata = Metadata(TestMetadata._TEST_VALUES)
        metadata.rename(1, 10)
        self.assertNotIn(1, metadata)
        self.assertEqual(metadata[10], 2)


if __name__ == "__main__":
    unittest.main()
