import os

from pyoram.core.chunk_file import ChunkFile
from pyoram.core.map import FileMap, PositionMap
from pyoram.core.oram import PathORAM
from pyoram.core.stash import Stash
from pyoram.crypto.aes_crypto import AESCrypto
from pyoram.crypto.keyfile import KeyFile
from pyoram import utils


def create_keys(pw):
    key_file = AESCrypto.create_keys(pw)
    key_file.save_to_file()


def verify_pw(pw):
    key_file = KeyFile.load_from_file()
    return AESCrypto(key_file, pw)


def setup_cloud():
    PathORAM().setup_cloud()


def setup_stash():
    Stash()


def get_uploaded_file_names():
    return FileMap().get_files()


def split_file_input(filename, file_input, aes_crypto):
    ChunkFile(aes_crypto).split(filename, file_input)


def delete_selected_node(filename):
    data_ids = FileMap().get_data_ids_of_file(filename)
    PositionMap().delete_data_ids(data_ids)
    Stash().delete_data_items(data_ids)
    FileMap().delete_file(filename)


def save_file(combined_file, path, filename_to_save_to):
    with open(os.path.join(path, filename_to_save_to), utils.WRITE_MODE) as file:
        file.write(combined_file)


def download_selected_file(selected_filename, path, filename_to_save_to, aes_crypto):
    data_ids = FileMap().get_data_ids_of_file(selected_filename)
    data_token = Stash().get_data_items(data_ids)
    # data_token[0] are the remaining data_ids, which are not stored in the stash
    remaining_data_ids = data_token[0]
    # data_token[1] are tuples of (data_id, data_item)
    data_items = data_token[1]
    if remaining_data_ids:
        leaf_ids = PositionMap().get_leaf_ids(remaining_data_ids)
        downloaded_data_items = PathORAM().download_data_items(remaining_data_ids, leaf_ids)
        data_items.extend(downloaded_data_items)

    # combining the data_items to a file starting with the lowest data_id
    data_items.sort()
    # TODO: handle error when data_items are missing
    combined_file = ChunkFile(aes_crypto).combine(data_items)
    # TODO: after decrypting encrypt the data again with new IV and store it with the same data_id in the stash
    save_file(combined_file, path, filename_to_save_to)
    # TODO: add logger for downloading
