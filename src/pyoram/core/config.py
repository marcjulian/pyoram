# Block size of the chunk files in terms of bytes
BLOCK_SIZE = 1000

# The height of the binary tree (as integer)
ORAM_LEVEL = 2

# dummy data id range
DUMMY_ID_START = 100000000000000
DUMMY_ID_STOP = 110000000000000

# for packing the data id
FORMAT_CHAR = '>Q'


def get_dummy_id_range():
    return range(DUMMY_ID_START, DUMMY_ID_STOP)
