from enum import Enum, unique


@unique
class ComparisonOperator(Enum):
    """
    Enums representing comparison operators.
    """
    EQUALS = "=",
    LESS_THAN = "<"
    GREATER_THAN = ">"
