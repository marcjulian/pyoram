import math
import random

# Block size of the chunk files in terms of bytes
BLOCK_SIZE = 1000

# The height of the binary tree (as integer)
# TODO: use height of 10 for testing
ORAM_LEVEL = 2
# The height of the binary tree (as integer)
LEAF_MIN = int(math.pow(2, ORAM_LEVEL) - 1)
LEAF_MAX = int(math.pow(2, ORAM_LEVEL + 1) - 2)

# dummy data id
DUMMY_ID = 999999999999999

# for packing the data id
FORMAT_CHAR = '>Q'


def get_random_leaf_id():
    return random.randrange(LEAF_MIN, LEAF_MAX + 1)
