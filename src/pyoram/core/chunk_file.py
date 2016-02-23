import logging
import base64

from pyoram import utils

# Block size of the chunk files in terms of bytes
BLOCK_SIZE = 1000


# TODO: calculate the block size for splitting the file, because the encryption makes the length bigger
# (also consider the dataID +  b"\x80"


class ChunkFile:
    def __init__(self, file_input, aes_crypto):
        # TODO: add file_map here to add new entries
        self.file_input = file_input
        self.aes_crypto = aes_crypto
        logging.info('length of the selected file %d ' % len(file_input))

    def split(self):
        for x in range(0, len(self.file_input), BLOCK_SIZE):
            chunk = self.file_input[x:BLOCK_SIZE + x]
            # TODO: padding of the last block if it doesn't fit the block size?
            # TODO: generate data item id (as int32 or int64) and add it to encrypt
            token = self.aes_crypto.encrypt(chunk)
            # TODO: save main_parts to a file in the stash
            main_parts = token[0]
            print(len(main_parts))
            # TODO: save iv and hmac in position map (or file map)
            iv = token[1]
            hmac = token[2]
