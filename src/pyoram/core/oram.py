import logging
import math

from pyoram.core import config
from pyoram.core.cloud import Cloud
from pyoram.core.map import PositionMap
from pyoram.core.stash import Stash
from pyoram.crypto.aes_crypto import AESCrypto, InvalidDataId


class PathORAM:
    def __init__(self, aes_crypto=None):
        self.cloud = Cloud()
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

    def access_oram(self, path_to_root):
        downloaded_data_items = self.read_path(path_to_root)
        self.write_stash(downloaded_data_items)
        self.write_path(path_to_root)

    def access_oram_with_stash(self, path_to_root, data_id):
        data_item = Stash().get_data_item(data_id)
        if not data_item:
            downloaded_data_items = self.read_path(path_to_root)
            data_item = self.write_stash(downloaded_data_items, data_id)
            self.write_path(path_to_root)
        return data_item

    def read_path(self, path_to_root):
        data_items = []
        for node in path_to_root:
            data_item = self.read_node(node)
            try:
                data_id = AESCrypto.retrieve_data_id(data_item)
                data_items.append((data_id, data_item))
                logging.info('[READ_PATH] download from node %d found data item with id %d' % (node, data_id))
            except InvalidDataId:
                # dummy data found
                logging.info('[READ_PATH] download from node %d found dummy data' % node)
                pass
        return data_items

    def write_path(self, path_to_root):
        for node in path_to_root:
            potential_data_properties = self.get_potential_data_ids_with_leaf()
            has_potential_item = False
            for potential_data_property in potential_data_properties:
                leaf_id = potential_data_property[1]
                potential_path = self.path_to_root(leaf_id)
                if node in potential_path:
                    has_potential_item = True
                    data_id = potential_data_property[0]
                    data_item = Stash().get_data_item(data_id)
                    logging.info('[WRITE PATH] upload to node %d data item with id %d' % (node, data_id))
                    self.write_node(node, data_item[1])
                    Stash().delete_data_item(data_id)
                    break
            if not has_potential_item:
                logging.info('[WRITE PATH] upload to node %d dummy data' % node)
                self.write_node(node)

    def write_stash(self, downloaded_data_items, data_id_of_interest=None):
        data_item_of_interest = None
        for downloaded_data_item in downloaded_data_items:
            data_id = downloaded_data_item[0]
            data_item = downloaded_data_item[1]
            iv, hmac = PositionMap().get_iv_and_hmac(data_id)
            plaintext = self.aes_crypto.decrypt(data_item, iv, hmac)
            token = self.aes_crypto.encrypt(plaintext, data_id)
            ciphertext = token[0]
            Stash().add_file(data_id, ciphertext)
            new_iv = token[1]
            new_hmac = token[2]
            if data_id_of_interest is not None and data_id_of_interest == data_id:
                PositionMap().update_data(data_id, new_iv, new_hmac, True)
                data_item_of_interest = data_id, plaintext
            else:
                PositionMap().update_data(data_id, new_iv, new_hmac)
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
            path_to_root = self.path_to_root(leaf_id)
            data_item = self.access_oram_with_stash(path_to_root, data_id)
            data_items.append(data_item)
        return data_items

    def update_data(self):
        # TODO: should only called for the first upload of a file, huge overhead otherwise
        for leaf in range(config.LEAF_MIN, config.LEAF_MAX + 1):
            path_to_root = self.path_to_root(leaf)
            self.access_oram(path_to_root)
