import math

from pyoram.core.chunk_file import BLOCK_SIZE
from pyoram.core.cloud import Cloud

# The height of the binary tree (as integer)
ORAM_LEVEL = 2


class PathORAM:
    def __init__(self):
        self.cloud = Cloud()

    @classmethod
    def get_max_oram_block_size(cls):
        return int(math.pow(2, ORAM_LEVEL + 1) - 1)

    @classmethod
    def get_max_oram_storage_size(cls):
        return cls.get_max_oram_block_size() * BLOCK_SIZE

    def setup_cloud(self):
        # TODO: setup_cloud only for the first time (how to identify the first time?)
        self.cloud.setup_cloud(self.get_max_oram_block_size())
