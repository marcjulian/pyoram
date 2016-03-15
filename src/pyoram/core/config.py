import random
import math

# Block size of the chunk files in terms of bytes
BLOCK_SIZE = 1000

# The height of the binary tree (as integer)
ORAM_LEVEL = 2
# The height of the binary tree (as integer)
LEAF_MIN = int(math.pow(2, ORAM_LEVEL) - 1)
LEAF_MAX = int(math.pow(2, ORAM_LEVEL + 1) - 2)

# dummy data id range
DUMMY_ID_START = 100000000000000
DUMMY_ID_STOP = 110000000000000

# for packing the data id
FORMAT_CHAR = '>Q'


def get_dummy_id_range():
    return range(DUMMY_ID_START, DUMMY_ID_STOP)


def get_random_leaf_id():
    return random.randrange(LEAF_MIN, LEAF_MAX + 1)
