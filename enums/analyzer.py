from enum import Enum


class IntensityEnum(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    EXTREME = 'EXTREME'


class UsageEnum(str, Enum):
    RACES = 'RACES'
    STABLE = 'STABLE'
    DECREASE = 'DECREASE'

    @classmethod
    def values(cls):
        return [usage_type for usage_type in cls]


class DecisionEnum(str, Enum):
    DELETE = 'DELETE'
    NORMAL = 'NORMAL'
    EXTEND = 'EXTEND'


class DimensionEnum(str, Enum):
    CPU = "CPU"
    RAM = "RAM"
    NETFLOW = "NetFlow"
