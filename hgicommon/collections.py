from typing import List

from hgicommon.models import Model, SearchCriterion


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


class Metadata(object):
    '''
    Generic key-value metadata model
    
    This is composed from a dictionary, rather than inheriting, in case
    the implementation needs to change and to expose only the methods
    used... Go figure :P
    '''
    def __init__(self):
        self._data = dict()

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return '{class_id} {representation}'.format(
            class_id = self.__class__,
            representation = str(self)
        )

    def __iter__(self):
        return self._data.__iter__()

    def get(self, key: str, default=None):
        '''
        Get item in metadata dictionary by its key, returning a fallback
        value when the key is not found

        @param  key      Dictionary key
        @param  default  Default value, if not found
        @return The value
        '''
        return self._data.get(key, default)

    def set(self, key: str, value):
        '''
        Set item in metadata dictionary by its key

        @param  key    Dictionary key
        @param  value  Value
        '''
        self._data[key] = value
