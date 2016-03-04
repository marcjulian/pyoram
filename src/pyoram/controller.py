from pyoram.crypto.aes_crypto import AESCrypto
from pyoram.crypto.keyfile import KeyFile
from pyoram.core.oram import PathORAM
from pyoram.core.stash import Stash
from pyoram.core.map import FileMap, PositionMap
from pyoram.core.chunk_file import ChunkFile


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
    ChunkFile(filename, file_input, aes_crypto).split()


def delete_selected_node(filename):
    data_ids = FileMap().get_data_ids_of_file(filename)
    PositionMap().delete_data_ids(data_ids)
    Stash().delete_data_items(data_ids)
    FileMap().delete_file(filename)


def download_selected_file(selected_filename, path, filename_to_save_to):
    data_ids = FileMap().get_data_ids_of_file(selected_filename)
    data_token = Stash().get_data_items(data_ids)
    # data_token[0] are the remaining data_ids, which are not stored in the stash
    remaining_data_ids = data_token[0]
    # data_token[1] are tuples of (data_id, data_item)
    data_items = data_token[1]
    if remaining_data_ids:
        # TODO: get the leaf_ids for the remaining data_ids from the position map
        # TODO: call ORAM to download the path, check which data is the corresponding data item for the data id,
        # TODO: ORAM should also upload some dummy data or something from the stash
        # TODO: add downloaded data_item tuple to data_items
        print('still data ids here')

    # combining the data_items to a file starting with the lowest data_id
    data_items.sort()
    # TODO: need aes_crypto in the signature to call chunk_file
    # TODO: decrypt and combine the data to one file, after decrypting encrypt the data again with new IV and store it with the same data_id in the stash
    # TODO: save the file to path and filename_to_save_to
    print('decrypt data_item')
    print('combine data_item now')
    print('save file to the location')
