import copy
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
        self._search_criteria = SearchCriteria([self._search_criterion1, self._search_criterion2])

    def test_init_with_same_attributes(self):
        self.assertRaises(ValueError, SearchCriteria, [self._search_criterion1, self._search_criterion1])

    def test_append_criterion_with_different_attributes(self):
        search_criteria = SearchCriteria()
        search_criteria.append(self._search_criterion1)
        search_criteria.append(self._search_criterion2)
        self.assertCountEqual(search_criteria, [self._search_criterion1, self._search_criterion2])

    def test_append_criterion_with_same_attributes(self):
        search_criteria = SearchCriteria()
        search_criteria.append(self._search_criterion1)
        self.assertRaises(ValueError, search_criteria.append, self._search_criterion1)

    def test_extend(self):
        search_criteria_1 = SearchCriteria([self._search_criterion1])
        search_criteria_2 = SearchCriteria([self._search_criterion2])
        search_criteria_1.extend(search_criteria_2)
        self.assertEqual(search_criteria_1, SearchCriteria([self._search_criterion1, self._search_criterion2]))

    def test_extend_with_same_attribute(self):
        search_criteria_1 = SearchCriteria([self._search_criterion1])
        search_criteria_2 = SearchCriteria([self._search_criterion1])
        self.assertRaises(ValueError, search_criteria_1.extend, search_criteria_2)

    def test_has_search_criteria_for_attribute_when_does_not(self):
        self.assertFalse(self._search_criteria.has_search_criteria_for_attribute("other"))

    def test_has_search_criteria_for_attribute_when_does(self):
        self.assertTrue(self._search_criteria.has_search_criteria_for_attribute(self._search_criterion1.attribute))

    def test_setitem(self):
        search_criteria = SearchCriteria([self._search_criterion1])
        search_criteria[0] = self._search_criterion2
        self.assertEqual(search_criteria, SearchCriteria([self._search_criterion2]))

    def test_setitem_with_same_attribute(self):
        def perform_test():
            self._search_criteria[1] = self._search_criterion1
        self.assertRaises(ValueError, perform_test)

    def test_setitem_replacing_self_with_self(self):
        self._search_criteria[0] = self._search_criterion1
        self.assertEqual(self._search_criteria, SearchCriteria([self._search_criterion1, self._search_criterion2]))

    def test_contains(self):
        self.assertIn(self._search_criterion1, self._search_criteria)
        self.assertNotIn(SearchCriterion("", "", ComparisonOperator.EQUALS), self._search_criteria)

    def test_str(self):
        string_representation = str(self._search_criteria)
        self.assertTrue(isinstance(string_representation, str))

    def test_repr(self):
        representation = repr(self._search_criteria)
        self.assertTrue(isinstance(representation, str))

    def test_del(self):
        del self._search_criteria[0]
        self.assertEqual(self._search_criteria, SearchCriteria([self._search_criterion2]))

    def test_delete_serach_criteria_for_attribute_when_not_exists(self):
        self.assertRaises(ValueError, self._search_criteria.delete_serach_criteria_for_attribute, "other")

    def test_delete_serach_criteria_for_attribute_when_exists(self):
        self._search_criteria.delete_serach_criteria_for_attribute(self._search_criterion1.attribute)
        self.assertEqual(self._search_criteria, SearchCriteria([self._search_criterion2]))


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
