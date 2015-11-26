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


class Metadata(object):
    '''
    Generic key-value metadata model
    
    This is composed from a dictionary, rather than inheriting, in case
    the implementation needs to change and to expose only the methods
    used...
    '''
    def __init__(self):
        self._data = dict()

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return '{class_id} {representation}'.format(
            class_id = self.__class__,
            representation = str(self)
        )

    def __eq__(self, other) -> bool:
        return self._data == other._data

    def __iter__(self):
        return self._data.__iter__()

    def has_attribute(self, attribute: str) -> bool:
        '''
        Check an attribute exists in the metadata

        @param  attribute  Dictionary key
        @return Exists in the dictionary
        '''
        return attribute in self._data

    def items(self):
        return self._data.items()

    def attributes(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def get(self, attribute: str, default=None):
        '''
        Get item in metadata by its attribute, returning a fallback
        value when the attribute is not found

        @param  attribute  Dictionary key
        @param  default    Default value, if not found
        @return The value
        '''
        return self._data.get(attribute, default)

    def __getitem__(self, attribute: str):
        return self.get(attribute)

    def set(self, attribute: str, value):
        '''
        Set item in metadata by its attribute

        @param  attribute  Dictionary key
        @param  value      Value
        '''
        self._data[attribute] = value

    def __setitem__(self, attribute: str, value):
        self.set(attribute, value)
