import logging
import math

from pyoram.exceptions import DummyFileFound
from pyoram.core import config
from pyoram.core.cloud import Cloud
from pyoram.core.map import PositionMap
from pyoram.core.stash import Stash


class PathORAM:
    def __init__(self, aes_crypto):
        self.cloud = Cloud(aes_crypto)
        self.aes_crypto = aes_crypto

    @classmethod
    def get_max_oram_block_size(cls):
        return int(math.pow(2, config.ORAM_LEVEL + 1) - 1)

    @classmethod
    def get_max_oram_storage_size(cls):
        return cls.get_max_oram_block_size() * config.BLOCK_SIZE

    def setup_cloud(self):
        self.cloud.setup_cloud(self.get_max_oram_block_size())

    # Find the path from root to leaf
    # __author__: Dr. Steve Gordon
    def path_to_leaf(self, leaf):
        path = [0] * (config.ORAM_LEVEL + 1)
        leafmin = config.LEAF_MIN
        leafmax = config.LEAF_MAX
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

    def get_potential_data_ids_with_leaf(self):
        potential_data_ids = Stash().get_potential_data_id()
        potential_data_properties = PositionMap().get_leaf_ids(potential_data_ids)
        return potential_data_properties

    def access_oram(self, path_to_root, data_id_of_interest=None):
        # TODO: start timer
        # TODO: lock the function to be used only in one thread at the time
        downloaded_data_items = self.read_path(path_to_root)
        data_item = self.write_stash(downloaded_data_items, data_id_of_interest)
        self.write_path(path_to_root)
        # TODO: end timer
        # TODO: statistics stash size
        return data_item

    def read_path(self, path_to_root):
        data_items = []
        for node in path_to_root:
            data_item = self.read_node(node)
            logging.info('[READ PATH] download from node %d' % node)
            data_items.append(data_item)
        return data_items

    def write_path(self, path_to_root):
        for node in path_to_root:
            potential_data_properties = self.get_potential_data_ids_with_leaf()
            has_potential_item = False
            for potential_data_property in potential_data_properties:
                potential_leaf_id = abs(potential_data_property[1])
                potential_path = self.path_to_root(potential_leaf_id)
                if node in potential_path:
                    has_potential_item = True
                    data_id = potential_data_property[0]
                    data_item = Stash().get_data_item(data_id)
                    logging.info('[WRITE PATH] upload to node %d data item with id %d' % (node, data_id))
                    self.write_node(node, data_item[1])
                    PositionMap().update_leaf_id(data_id, True)
                    Stash().delete_data_item(data_id)
                    break
            if not has_potential_item:
                logging.info('[WRITE PATH] upload to node %d dummy data' % node)
                self.write_node(node)

    def decrypt_data_item(self, data_item):
        return self.aes_crypto.decrypt(data_item)

    def write_stash(self, downloaded_data_items, data_id_of_interest=None):
        data_item_of_interest = None
        for downloaded_data_item in downloaded_data_items:
            try:
                data_id, plaintext = self.decrypt_data_item(downloaded_data_item)
                # TODO: if data id is not in the position map, skip the data item
                logging.info('[WRITE STASH] downloaded data item with id %d' % data_id)
                token = self.aes_crypto.encrypt(plaintext, data_id)
                Stash().add_file(data_id, token)
                if data_id_of_interest is not None and data_id_of_interest == data_id:
                    PositionMap().choose_new_leaf_id(data_id)
                    data_item_of_interest = data_id, plaintext
                else:
                    PositionMap().update_leaf_id(data_id, False)
            except DummyFileFound:
                logging.info('[WRITE STASH] downloaded dummy file')
                pass
        return data_item_of_interest

    def read_node(self, node):
        return self.cloud.download_node(node)

    def write_node(self, node, data_item=None):
        self.cloud.upload_to_node(node, data_item)

    def download_data_items(self, data_properties):
        data_items = []
        for data_property in data_properties:
            data_id = data_property[0]
            leaf_id = data_property[1]
            if leaf_id < 0:
                data_item = Stash().get_data_item(data_id)
                logging.info('[PATH ORAM] access stash')
                # decrypt data item
                data_item = self.decrypt_data_item(data_item[1])
                data_items.append(data_item)
            else:
                path_to_root = self.path_to_root(leaf_id)
                data_item = self.access_oram(path_to_root, data_id)
                data_items.append(data_item)
        return data_items

    def update_data(self, data_properties):
        for data_property in data_properties:
            leaf_id = abs(data_property[1])
            path_to_root = self.path_to_root(leaf_id)
            self.access_oram(path_to_root)
