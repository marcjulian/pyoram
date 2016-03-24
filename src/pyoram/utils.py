import base64

WRITE_MODE = 'w'
READ_MODE = 'r'
READ_WRITE_MODE = 'r+'
READ_BINARY_MODE = 'rb'
WRITE_BINARY_MODE = 'wb'

KEY_MAP_FILE_NAME = 'key.map'
FILE_MAP_FILE_NAME = 'file.map'
POSITION_MAP_FILE_NAME = 'position.map'
STASH_FOLDER_NAME = 'stash'

CLOUD_MAP_FILE_NAME = 'cloud.map'

LOG_FILE_NAME = 'pyoram.log'


def str_to_byte(att):
    return att.encode()


def byte_to_str(att):
    return att.decode()
