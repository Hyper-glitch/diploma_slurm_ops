from enum import Enum


class IntensityEnum(Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    EXTREME = 'EXTREME'


class UsageEnum(Enum):
    RACES = 'RACES'
    STABLE = 'STABLE'
    DECREASE = 'DECREASE'

    @classmethod
    def values(cls):
        return [usage_type.value for usage_type in cls]


class DecisionEnum(Enum):
    DELETE = 'DELETE'
    NORMAL = 'NORMAL'
    EXTEND = 'EXTEND'
