import logging

from pyoram.core import config
from pyoram.core.map import FileMap, PositionMap
from pyoram.core.stash import Stash
from pyoram.exceptions import FileSizeError


# TODO: calculate the block size for splitting the file, because the encryption makes the length bigger
# (also consider the dataID +  b"\x80")
class ChunkFile:
    def __init__(self, aes_crypto=None):
        self.aes_crypto = aes_crypto
        self.data_id_counter = FileMap().get_id_counter()

    def split(self, file_name, file_input):
        logging.info('length of the selected file %d ' % len(file_input))
        data_ids = []
        for x in range(0, len(file_input), config.BLOCK_SIZE):
            if self.data_id_counter == config.DUMMY_ID:
                self.data_id_counter += 1
            data_id = self.data_id_counter
            self.data_id_counter += 1
            data_ids.append(data_id)
            chunk = file_input[x:config.BLOCK_SIZE + x]
            logging.info('[CHUNK FILE] chunk size is %d after splitting' % len(chunk))
            if len(chunk) != config.BLOCK_SIZE:
                # TODO: padding of the last block if it doesn't fit the block size?
                logging.info('[CHUNK FILE] chunk is smaller than the block size, add padding here')
            token = self.aes_crypto.encrypt(chunk, data_id)
            logging.info('[CHUNK FILE] chunk size is %d after encryption' % len(token))
            Stash().add_file(data_id, token)
            PositionMap().add_data(data_id)
        FileMap().add_file(file_name, len(file_input), data_ids, self.data_id_counter)

    def combine(self, data_items, expected_file_len):
        plaintext = bytearray()
        for data_item in data_items:
            logging.info('[CHUNK FILE] combining data item with id %d' % data_item[0])
            plaintext.extend(data_item[1])

        if expected_file_len != len(plaintext):
            raise FileSizeError('File size of the downloaded file is not correct.')

        return plaintext
