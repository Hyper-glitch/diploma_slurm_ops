from enum import Enum


class UsageEnum(str, Enum):
    RACES = 'RACES'
    STABLE = 'STABLE'
    DECREASE = 'DECREASE'

    @classmethod
    def values(cls):
        return [usage_type for usage_type in cls]
