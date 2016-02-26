import logging
import os

from pyoram import utils
from pyoram.core.map import FileMap, PositionMap
from pyoram.core.stash import Stash

# Block size of the chunk files in terms of bytes
BLOCK_SIZE = 1000


# TODO: calculate the block size for splitting the file, because the encryption makes the length bigger
# (also consider the dataID +  b"\x80")
class ChunkFile:
    def __init__(self, file_name, file_input, aes_crypto):
        self.file_name = file_name
        self.file_input = file_input
        self.aes_crypto = aes_crypto
        self.file_size = len(file_input)
        # TODO: retrieve highest number from filemap
        self.data_id_counter = 0
        logging.info('length of the selected file %d ' % len(file_input))

    def split(self):
        data_items = []
        for x in range(0, len(self.file_input), BLOCK_SIZE):
            # TODO: generate data item id (as int32 or int64) and add it to encrypt
            data_id = self.data_id_counter
            self.data_id_counter += 1
            data_items.append(data_id)
            chunk = self.file_input[x:BLOCK_SIZE + x]
            if len(chunk) != BLOCK_SIZE:
                # TODO: padding of the last block if it doesn't fit the block size?
                logging.info('chunk is smaller than the block size, add padding here')
            token = self.aes_crypto.encrypt(chunk, utils.str_to_byte(str(data_id)))
            main_part = token[0]
            Stash().add_file(data_id, utils.byte_to_str(main_part))
            iv = token[1]
            hmac = token[2]
            PositionMap().add_data(data_id, iv, hmac)
        FileMap().add_file(self.file_name, self.file_size, data_items)
