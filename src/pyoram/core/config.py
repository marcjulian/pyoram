import math
import random
from enum import Enum

# Block size of the chunk files in terms of bytes
BLOCK_SIZE = 1000

# The height of the binary tree (as integer)
# TODO: use height of 5 to 10 for testing
ORAM_LEVEL = 5

# The height of the binary tree (as integer)
LEAF_MIN = int(math.pow(2, ORAM_LEVEL) - 1)
LEAF_MAX = int(math.pow(2, ORAM_LEVEL + 1) - 2)

# dummy data id
DUMMY_ID = 999999999999999

# for packing the data id
FORMAT_CHAR = '>Q'


class DataType(Enum):
    kB = 1000
    MB = 1000000
    GB = 1000000000
    TB = 1000000000000

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value


def get_random_leaf_id():
    return random.randrange(LEAF_MIN, LEAF_MAX + 1)


def get_format(storage):
    data_type_name = None
    data_type_value = None

    if storage <= DataType.MB.get_value():
        data_type_name = DataType.kB.get_name()
        data_type_value = DataType.kB.get_value()
    elif storage < DataType.GB.get_value():
        data_type_name = DataType.MB.get_name()
        data_type_value = DataType.MB.get_value()
    elif storage < DataType.TB.get_value():
        data_type_name = DataType.GB.get_name()
        data_type_value = DataType.GB.get_value()
    elif storage >= DataType.TB.get_value():
        data_type_name = DataType.TB.get_name()
        data_type_value = DataType.TB.get_value()

    return data_type_name, data_type_value
