from abc import ABCMeta
from enum import Enum, unique
from typing import Generic, TypeVar

from hgicommon.enums import ComparisonOperator


class Model(metaclass=ABCMeta):
    """
    Superclass that all POPOs (Plain Old Python Objects) must implement.
    """
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for property_name, value in vars(self).items():
            if other.__dict__[property_name] != self.__dict__[property_name]:
                return False
        return True

    def __str__(self) -> str:
        string_builder = []
        for property, value in vars(self).items():
            string_builder.append("%s: %s" % (property, value))
        return "{ %s }" % ', '.join(string_builder)

    def __repr__(self) -> str:
        return "<%s object at %s: %s>" % (type(self), id(self), str(self))

    def __hash__(self):
        return hash(str(self))


class SearchCriterion(Model):
    """
    Model of an attribute search criterion.
    """
    def __init__(self, attribute: str, value: str, comparison_operator: ComparisonOperator):
        self.attribute = attribute
        self.value = value
        self.comparison_operator = comparison_operator


# The type of the object that is registered
_RegistrationTarget = TypeVar("RegistrationTarget")


class RegistrationEvent(Generic[_RegistrationTarget], Model):
    """
    A model of a registration update.
    """
    @unique
    class Type(Enum):
        """
        The type of event.
        """
        REGISTERED = 0
        UNREGISTERED = 1

    def __init__(self, target: _RegistrationTarget, event_type: Type):
        """
        Constructor.
        :param target: the object the event refers to
        :param event_type: the type of update event
        """
        self.target = target
        self.event_type = event_type
