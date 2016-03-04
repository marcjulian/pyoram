import logging

from pyoram import utils
from pyoram.core import config
from pyoram.core.map import FileMap, PositionMap
from pyoram.core.stash import Stash


# TODO: calculate the block size for splitting the file, because the encryption makes the length bigger
# (also consider the dataID +  b"\x80")
class ChunkFile:
    def __init__(self, file_name, file_input, aes_crypto):
        # TODO: change so it can be used for splitting and combining
        self.file_name = file_name
        self.file_input = file_input
        self.aes_crypto = aes_crypto
        self.file_size = len(file_input)
        self.data_id_counter = FileMap().get_id_counter()
        logging.info('length of the selected file %d ' % len(file_input))

    def split(self):
        # TODO: add filename and file_input to signature
        data_items = []
        for x in range(0, len(self.file_input), config.BLOCK_SIZE):
            # TODO: generate data item id (as int32 or int64) and add it to encrypt
            data_id = self.data_id_counter
            self.data_id_counter += 1
            data_items.append(data_id)
            chunk = self.file_input[x:config.BLOCK_SIZE + x]
            if len(chunk) != config.BLOCK_SIZE:
                # TODO: padding of the last block if it doesn't fit the block size?
                logging.info('chunk is smaller than the block size, add padding here')
            token = self.aes_crypto.encrypt(chunk, utils.str_to_byte(str(data_id)))
            main_part = token[0]
            Stash().add_file(data_id, utils.byte_to_str(main_part))
            iv = token[1]
            hmac = token[2]
            PositionMap().add_data(data_id, utils.byte_to_str(iv), utils.byte_to_str(hmac))
        FileMap().add_file(self.file_name, self.file_size, data_items, self.data_id_counter)

    def combine(self):
        # TODO: check if the data block is part of the file (check data id), than encrypt data and append the plaintext
        print('combine chunk files')
