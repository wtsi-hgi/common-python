from typing import List

from hgicommon.models import SearchCriterion


class SearchCriteria(list):
    """
    A collection of `SearchCriteria`.
    """
    def __init__(self, search_criterion_list: List[SearchCriterion]=()):
        super(SearchCriteria, self).__init__()
        for search_criterion in search_criterion_list:
            self.append(search_criterion)

    def append(self, search_criterion: SearchCriterion):
        for existing_search_criterion in self:
            if existing_search_criterion.attribute == search_criterion.attribute:
                raise ValueError("Search criterion based on the attribute `%s` already added")

        super(SearchCriteria, self).append(search_criterion)


class Metadata(dict):
    """
    Self-canonicalising dictionary for metadata.
    """
    def __init__(self, base=None, **kwargs):
        """
        Override constructor, so base and kwargs are canonicalised.
        """
        super(Metadata, self).__init__(**kwargs)
        if base and type(base) is dict:
            for key, value in base.items():
                self.__setitem__(key, value)

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __setitem__(self, key, value):
        """
        Override __setitem__, so scalar values are put into a list and lists are sorted and made unique.

        n.b., We assume our dictionaries are only one deep.
        """
        if type(value) is list:
            super().__setitem__(key, sorted(set(value)))
        else:
            super().__setitem__(key, [value])
