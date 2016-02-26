import data
import json

from pyoram import utils

JSON_FILE = 'files'
JSON_FILE_NAME = 'file_name'
JSON_FILE_SIZE = 'file_size'
JSON_DATA_ITEMS = 'data_items'


class FileMap:
    def __init__(self):
        if not data.file_exists(utils.FILE_MAP_FILE_NAME):
            with data.open_data_file(utils.FILE_MAP_FILE_NAME, utils.WRITE_MODE) as file_map:
                json.dump((), file_map, indent=2)

    def add_file(self, file_name, file_size, data_items):
        with data.open_data_file(utils.FILE_MAP_FILE_NAME, utils.READ_WRITE_MODE) as file_map:
            file_data = json.load(file_map)
            file_data.append({JSON_FILE_NAME: file_name, JSON_FILE_SIZE: file_size, JSON_DATA_ITEMS: data_items})
            file_map.seek(0)
            json.dump(file_data, file_map, indent=2, sort_keys=True)
            file_map.truncate()


class PositionMap:
    # fields in the positionmap: dataId, leafID, iv, hash
    # leafID is random
    def __init__(self):
        if not data.file_exists(utils.POSITION_MAP_FILE_NAME):
            with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.WRITE_MODE) as position_map:
                json.dump({}, position_map, indent=2)

    def add_data(self, data_id, iv, hmac):
        # TODO: generate random leaf_id
        print('add data')
