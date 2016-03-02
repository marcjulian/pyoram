from pyoram.crypto.aes_crypto import AESCrypto
from pyoram.crypto.keyfile import KeyFile
from pyoram.core.oram import PathORAM
from pyoram.core.stash import Stash
from pyoram.core.map import FileMap
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
