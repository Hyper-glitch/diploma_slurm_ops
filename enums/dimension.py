from enum import Enum


class DimensionEnum(str, Enum):
    CPU = "CPU"
    RAM = "RAM"
    NETFLOW = "NetFlow"
