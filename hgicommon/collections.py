from typing import Sequence

from hgicommon.models import SearchCriterion


class SearchCriteria(list):
    """
    A collection of `SearchCriterion`.
    """
    _DUPLICATE_ERROR_MESSAGE = "Search criterion based on the attribute `%s` already added"

    def __init__(self, search_criterion_list: Sequence[SearchCriterion]=()):
        super(SearchCriteria, self).__init__()
        for search_criterion in search_criterion_list:
            self.append(search_criterion)

    def append(self, search_criterion: SearchCriterion):
        for existing_search_criterion in self:
            if existing_search_criterion.attribute == search_criterion.attribute:
                raise ValueError(SearchCriteria._DUPLICATE_ERROR_MESSAGE)

        super(SearchCriteria, self).append(search_criterion)

    def extend(self, iterable):
        for search_criteria in iterable:
            self.append(search_criteria)

    def __setitem__(self, key, value):
        count = self.count(value)
        if count > 1 or (count == 1 and self.index(value) != key):
            raise ValueError(SearchCriteria._DUPLICATE_ERROR_MESSAGE)
        super(SearchCriteria, self).__setitem__(key, value)

    def __add__(self, other):
        for search_criteria in other:
            self.append(search_criteria)
