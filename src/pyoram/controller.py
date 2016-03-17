import logging
import os

from pyoram import utils
from pyoram.core.chunk_file import ChunkFile
from pyoram.core.map import FileMap, PositionMap
from pyoram.core.oram import PathORAM
from pyoram.core.stash import Stash
from pyoram.crypto.aes_crypto import AESCrypto
from pyoram.crypto.keyfile import KeyFile
from pyoram.exceptions import DownloadFileError


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


def save_file_input(filename, file_input, aes_crypto):
    logging.info('Start upload of file %s', filename)
    ChunkFile(aes_crypto).split(filename, file_input)


def update_data(aes_crypto):
    PathORAM(aes_crypto).update_data()
    logging.info('End upload of file')


def delete_selected_node(filename):
    data_ids = FileMap().get_data_ids_of_file(filename)
    PositionMap().delete_data_ids(data_ids)
    Stash().delete_data_items(data_ids)
    FileMap().delete_file(filename)


def save_file(combined_file, path, filename_to_save_to):
    with open(os.path.join(path, filename_to_save_to), utils.WRITE_BINARY_MODE) as file:
        file.write(combined_file)


def download_selected_file(selected_filename, path, filename_to_save_to, aes_crypto):
    logging.info('Start download of file %s', selected_filename)
    data_ids = FileMap().get_data_ids_of_file(selected_filename)
    data_properties = PositionMap().get_leaf_ids(data_ids)
    downloaded_data_items = PathORAM(aes_crypto).download_data_items(data_properties)

    if len(data_ids) != len(downloaded_data_items):
        raise DownloadFileError('An error occurred during file download')

    combined_file = ChunkFile().combine(downloaded_data_items, FileMap().get_file_len(selected_filename))
    save_file(combined_file, path, filename_to_save_to)
    logging.info('End download of file %s', selected_filename)
