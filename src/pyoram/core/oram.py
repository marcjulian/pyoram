import math
import random

from pyoram.core import config
from pyoram.core.cloud import Cloud

# The height of the binary tree (as integer)
LEAF_MIN = int(math.pow(2, config.ORAM_LEVEL) - 1)
LEAF_MAX = int(math.pow(2, config.ORAM_LEVEL + 1) - 2)


# TODO: add ORAM functions here: downloading a path, uploading a file to the cloud
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

    # Find the path from root to leaf
    # __author__: Dr. Steve Gordon
    def path_to_leaf(self, leaf):
        path = [0] * (config.ORAM_LEVEL + 1)
        leafmin = LEAF_MIN
        leafmax = LEAF_MAX
        for curlevel in range(config.ORAM_LEVEL):
            mid = (leafmax - leafmin) // 2 + leafmin
            if leaf <= mid:
                path[curlevel + 1] = path[curlevel] * 2 + 1
                leafmax = mid
            else:
                path[curlevel + 1] = path[curlevel] * 2 + 2
                leafmin = mid + 1
        return path

    # Find the path from leaf to root
    # __author__: Dr. Steve Gordon
    def path_to_root(self, leaf):
        path = self.path_to_leaf(leaf)
        path.reverse()
        return path

    def access_oram(self, path_to_root, data_ids=None):
        # TODO: read path (return data items of the path, real data will be stored in the stash or used for combining)
        for node in path_to_root:
            print('downloading node %s' % node)
            self.cloud.download_node(node)
        # TODO: write path (choose data from the stash otherwise create dummy data)
        # TODO: return tuple (data_ids, data_item), when should it be encrypted and check for the data id?
        pass

    def download_data_items(self, remaining_data_ids, leaf_ids):
        data_items = []
        for leaf_id in leaf_ids:
            path_to_root = self.path_to_root(leaf_id)
            self.access_oram(path_to_root, remaining_data_ids)
        # add data item with data id: data_items.append((data_id, data_item))
        # TODO: call ORAM to download the path, check which data is the corresponding data item for the data id,
        # TODO: ORAM should also upload some dummy data or something from the stash
        return data_items
