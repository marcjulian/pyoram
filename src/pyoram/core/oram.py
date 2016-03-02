import math
import random

from pyoram.core import config
from pyoram.core.cloud import Cloud

# The height of the binary tree (as integer)
LEAF_MIN = int(math.pow(2, config.ORAM_LEVEL) - 1)
LEAF_MAX = int(math.pow(2, config.ORAM_LEVEL + 1) - 2)


class PathORAM:
    def __init__(self):
        self.cloud = Cloud()

    @classmethod
    def get_max_oram_block_size(cls):
        return int(math.pow(2, config.ORAM_LEVEL + 1) - 1)

    @classmethod
    def get_max_oram_storage_size(cls):
        return cls.get_max_oram_block_size() * config.BLOCK_SIZE

    def setup_cloud(self):
        self.cloud.setup_cloud(self.get_max_oram_block_size())

    @classmethod
    def get_random_leaf_id(cls):
        return random.randrange(LEAF_MIN, LEAF_MAX + 1)
