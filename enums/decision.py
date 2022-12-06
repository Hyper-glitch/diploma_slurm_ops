from enum import Enum


class DecisionEnum(str, Enum):
    DELETE = "DELETE"
    NORMAL = "NORMAL"
    EXTEND = "EXTEND"
