import base64
import json
import logging
import os
import random
import struct

import dropbox

import data
from pyoram import utils
from pyoram.core import config
from pyoram.exceptions import ErrorInCloudMap

JSON_TOKEN = 'token'
JSON_INIT = 'init'
TOKEN_PLACEHOLDER = 'My token'
FILE_NAME = 'block%d.oram'
RANDOM_BYTE_FACTOR = 0.74

RESPONSE_CODE_OK = 200


class Cloud:
    def __init__(self):
        if not data.file_exists(utils.CLOUD_MAP_FILE_NAME):
            logging.info('Create cloud map')
            self.create_cloud_map()
        cloud_map = self.load_cloud_map()
        self.token = cloud_map[0]
        self.cloud_init = cloud_map[1]
        self.dbx = dropbox.Dropbox(self.token)

    def create_cloud_map(self):
        with data.open_data_file(utils.CLOUD_MAP_FILE_NAME, utils.WRITE_MODE) as cloud_map:
            json.dump({JSON_TOKEN: TOKEN_PLACEHOLDER, JSON_INIT: False}, cloud_map, indent=2)

    def load_cloud_map(self):
        with data.open_data_file(utils.CLOUD_MAP_FILE_NAME, utils.READ_MODE) as cloud_map:
            try:
                cloud_data = json.load(cloud_map)
                return cloud_data[JSON_TOKEN], cloud_data[JSON_INIT]
            except(ValueError, KeyError):
                logging.warning('Error in cloud map.')
                raise ErrorInCloudMap('Error in cloud map.')

    def update_cloud_map(self):
        with data.open_data_file(utils.CLOUD_MAP_FILE_NAME, utils.READ_WRITE_MODE) as cloud_map:
            cloud_data = json.load(cloud_map)
            cloud_data[JSON_INIT] = self.cloud_init
            cloud_map.seek(0)
            json.dump(cloud_data, cloud_map, indent=2)
            cloud_map.truncate()

    @classmethod
    def get_random_byte_len(cls):
        return int(RANDOM_BYTE_FACTOR * config.BLOCK_SIZE)

    def setup_cloud(self, max_block_size):
        if not self.cloud_init:
            logging.info('Cloud is not initialized')
            logging.info('start setup of the cloud')
            for block in range(0, max_block_size):
                logging.info('upload file %d' % block)
                self.dbx.files_upload(self.create_dummy_data(), self.create_path_name(block))
            logging.info('end setup of the cloud')
            self.cloud_init = True
            self.update_cloud_map()

    def create_dummy_data(self):
        dummy_id = random.randrange(config.DUMMY_ID_START, config.DUMMY_ID_STOP)
        dummy_data = (
            os.urandom(self.get_random_byte_len()) + struct.pack(config.FORMAT_CHAR, dummy_id)
        )
        return base64.urlsafe_b64encode(dummy_data).decode()

    def download_node(self, node):
        # response token is a tuple of: dropbox.files.FileMetadata, requests.models.Response
        response_token = self.dbx.files_download(self.create_path_name(node))
        # Response model carries the content
        response = response_token[1]
        if response.status_code == RESPONSE_CODE_OK:
            return response.content
        return None

    def upload_to_node(self, node, content=None):
        if content is None:
            content = self.create_dummy_data()
        self.dbx.files_upload(content, self.create_path_name(node), mode=dropbox.files.WriteMode.overwrite)

    def create_path_name(self, node):
        return '/' + FILE_NAME % node
