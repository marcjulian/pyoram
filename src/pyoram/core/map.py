import data
import json

from pyoram import utils
from pyoram.core.oram import PathORAM

# file.map
JSON_FILES = 'files'
JSON_ID_COUNTER = 'counter'
JSON_FILE_NAME = 'file_name'
JSON_FILE_SIZE = 'file_size'
JSON_DATA_ITEMS = 'data_items'

# position.map
JSON_LEAF_ID = 'leaf_id'
JSON_DATA_ID = 'data_id'
JSON_IV = 'iv'
JSON_HMAC = 'hmac'


class FileMap:
    def __init__(self):
        if not data.file_exists(utils.FILE_MAP_FILE_NAME):
            with data.open_data_file(utils.FILE_MAP_FILE_NAME, utils.WRITE_MODE) as file_map:
                json.dump({JSON_FILES: (), JSON_ID_COUNTER: 0}, file_map, indent=2)

    def add_file(self, file_name, file_size, data_items, data_id_counter):
        with data.open_data_file(utils.FILE_MAP_FILE_NAME, utils.READ_WRITE_MODE) as file_map:
            file_data = json.load(file_map)
            file_data[JSON_FILES].append(
                {JSON_FILE_NAME: file_name, JSON_FILE_SIZE: file_size, JSON_DATA_ITEMS: data_items})
            # updating the data id counter
            file_data[JSON_ID_COUNTER] = data_id_counter
            file_map.seek(0)
            json.dump(file_data, file_map, indent=2, sort_keys=True)
            file_map.truncate()

    def get_files(self):
        file_names = []
        with data.open_data_file(utils.FILE_MAP_FILE_NAME, utils.READ_MODE) as file_map:
            file_data = json.load(file_map)
            for file in file_data[JSON_FILES]:
                file_names.append(file[JSON_FILE_NAME])
            return file_names

    def get_id_counter(self):
        with data.open_data_file(utils.FILE_MAP_FILE_NAME, utils.READ_MODE) as file_map:
            file_data = json.load(file_map)
            return file_data[JSON_ID_COUNTER]


class PositionMap:
    def __init__(self):
        if not data.file_exists(utils.POSITION_MAP_FILE_NAME):
            with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.WRITE_MODE) as position_map:
                json.dump((), position_map, indent=2)

    def add_data(self, data_id, iv, hmac):
        with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.READ_WRITE_MODE) as position_map:
            position_data = json.load(position_map)
            position_data.append(
                {JSON_LEAF_ID: PathORAM.get_random_leaf_id(), JSON_DATA_ID: data_id, JSON_IV: iv, JSON_HMAC: hmac})
            position_map.seek(0)
            json.dump(position_data, position_map, indent=2, sort_keys=True)
