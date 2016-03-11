import math
import random

from pyoram.core import config
from pyoram.core.cloud import Cloud
from pyoram.crypto.aes_crypto import AESCrypto, InvalidDataId
from pyoram.core.stash import Stash

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

    def access_oram(self, path_to_root):
        downloaded_data_items = self.read_path(path_to_root)
        self.write_stash(downloaded_data_items)
        self.write_path(path_to_root)

    def access_oram_with_stash(self, path_to_root, data_id):
        data_item = Stash().get_data_item(data_id)
        # TODO: call stash
        if not data_item:
            # TODO: call read path
            # TODO: call write stash (include decrypting and re-encrypting)
            # TODO: call write path
            print('woop')

        return data_item

    def read_path(self, path_to_root):
        data_items = []
        for node in path_to_root:
            data_item = self.read_node(node)
            try:
                data_id = AESCrypto.retrieve_data_id(data_item)
                data_items.append((data_id, data_item))
            except InvalidDataId:
                # dummy data found
                pass
        return data_items

    def write_path(self, path_to_root):
        for node in path_to_root:
            # TODO: get random content from stash, which would fit into the node based on the leaf id
            self.write_node(node)

    def write_stash(self, downloaded_data_items):
        for downloaded_data_item in downloaded_data_items:
            print('write to stash')

    def read_node(self, node):
        return self.cloud.download_node(node)

    def write_node(self, node):
        self.cloud.upload_to_node(node)

    def download_data_items(self, data_properties):
        data_items = []
        for data_property in data_properties:
            data_id = data_property[0]
            leaf_id = data_property[1]
            path_to_root = self.path_to_root(leaf_id)
            data_item = self.access_oram_with_stash(path_to_root, data_id)
            data_items.append(data_item)
        return data_items

    def update_data(self):
        for leaf in range(LEAF_MIN, LEAF_MAX + 1):
            path_to_root = self.path_to_root(leaf)
            self.access_oram(path_to_root)
