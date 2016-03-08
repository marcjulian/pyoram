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
        data_items = []
        for node in path_to_root:
            # TODO: return data items, if the data id is in data ids otherwise store it in the stash
            # TODO: check for data id
            data_item = self.read_node(node)
            # TODO: add to data_items if the id is in data_ids
            # TODO: add to stash anyways (but drop dummy data)
        for node in path_to_root:
            self.write_node(node)
            # TODO: return tuple (data_ids, data_item)

    def read_node(self, node):
        print('downloading node %s' % node)
        return self.cloud.download_node(node)

    def write_node(self, node):
        self.cloud.upload_node(node)

    def download_data_items(self, remaining_data_ids, leaf_ids):
        data_items = []
        for leaf_id in leaf_ids:
            path_to_root = self.path_to_root(leaf_id)
            self.access_oram(path_to_root, remaining_data_ids)
        # add data item with data id: data_items.append((data_id, data_item))
        return data_items
