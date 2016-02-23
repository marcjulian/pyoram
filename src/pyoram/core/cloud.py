import dropbox
import data
import json
import os
import base64
import logging

from pyoram import utils
from pyoram.exceptions import ErrorInCloudMap
from pyoram.core.chunk_file import BLOCK_SIZE

JSON_TOKEN = 'token'
FILE_NAME = 'block%d.oram'
RANDOM_BYTE_FACTOR = 0.75


class Cloud:
    def __init__(self):
        self.dbx = dropbox.Dropbox(self.load_token())

    def load_token(self):
        cloud_map = data.open_data_file(utils.CLOUD_MAP_FILE_NAME, utils.READ_MODE)
        try:
            json_cloud_map = json.load(cloud_map)
            return json_cloud_map[JSON_TOKEN]
        except(ValueError, KeyError):
            logging.warning('Error in cloud map.')
            raise ErrorInCloudMap('Error in cloud map.')
        finally:
            cloud_map.close()

    @classmethod
    def get_random_byte_len(cls):
        return int(RANDOM_BYTE_FACTOR * BLOCK_SIZE)

    def setup_cloud(self, max_block_size):
        logging.info('start setup of the cloud')
        for block in range(0, max_block_size):
            logging.info('upload file %d' % block)
            self.dbx.files_upload(base64.urlsafe_b64encode(os.urandom(self.get_random_byte_len())).decode(),
                                  '/' + FILE_NAME % block)
        # TODO: write init is done to one of the maps, so that init is not necessary again
        logging.info('end setup of the cloud')
