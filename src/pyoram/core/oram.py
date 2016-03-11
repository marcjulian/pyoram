import math
import random

from pyoram.core import config
from pyoram.core.cloud import Cloud
from pyoram.crypto.aes_crypto import AESCrypto, InvalidDataId

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
        # TODO: should data_items_stash be global?
        data_items_stash = []
        # TODO: move the for loop to read_node
        for node in path_to_root:
            data_item = self.read_node(node)
            try:
                data_id = AESCrypto.retrieve_data_id(data_item)
                if data_id in data_ids:
                    data_items.append((data_id, data_item))
                data_items_stash.append((data_id, data_item))
                # TODO: save the data_items to the stash before write_node
                # TODO: before saving the data items into the stash, decrypt and re-encrypt with a new iv
            except InvalidDataId:
                # dummy data found
                pass
        # TODO: move the for loop to write_node
        for node in path_to_root:
            self.write_node(node)
        return data_items

    def read_node(self, node):
        return self.cloud.download_node(node)

    def write_node(self, node):
        # TODO: get random content from stash, which would fit into the node based on the leaf id
        self.cloud.upload_to_node(node)

    def download_data_items(self, remaining_data_ids, leaf_ids):
        data_items = []
        for leaf_id in leaf_ids:
            path_to_root = self.path_to_root(leaf_id)
            data_items.extend(self.access_oram(path_to_root, remaining_data_ids))
        return data_items

    def update_data(self):
        # TODO: triggered by upload a new file
        # TODO: access oram
        pass
