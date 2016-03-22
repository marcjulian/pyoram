import json

import data
from pyoram import utils
from pyoram.core import config

# file.map
JSON_FILES = 'files'
JSON_ID_COUNTER = 'counter'
JSON_FILE_NAME = 'file_name'
JSON_FILE_SIZE = 'file_size'
JSON_DATA_ITEMS = 'data_items'

# position.map
JSON_LEAF_ID = 'leaf_id'
JSON_DATA_ID = 'data_id'


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

    def get_data_ids_of_file(self, filename):
        with data.open_data_file(utils.FILE_MAP_FILE_NAME, utils.READ_MODE) as file_map:
            file_data = json.load(file_map)
            for file in file_data[JSON_FILES]:
                if file[JSON_FILE_NAME] == filename:
                    return file[JSON_DATA_ITEMS]

    def get_file_len(self, filename):
        with data.open_data_file(utils.FILE_MAP_FILE_NAME, utils.READ_MODE) as file_map:
            file_data = json.load(file_map)
            for file in file_data[JSON_FILES]:
                if file[JSON_FILE_NAME] == filename:
                    return file[JSON_FILE_SIZE]

    def delete_file(self, filename):
        with data.open_data_file(utils.FILE_MAP_FILE_NAME, utils.READ_WRITE_MODE) as file_map:
            file_data = json.load(file_map)
            files = file_data[JSON_FILES]
            for entry in list(files):
                if entry[JSON_FILE_NAME] == filename:
                    files.remove(entry)
                    break
            file_map.seek(0)
            json.dump(file_data, file_map, indent=2, sort_keys=True)
            file_map.truncate()


class PositionMap:
    def __init__(self):
        if not data.file_exists(utils.POSITION_MAP_FILE_NAME):
            with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.WRITE_MODE) as position_map:
                json.dump((), position_map, indent=2)

    def add_data(self, data_id):
        with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.READ_WRITE_MODE) as position_map:
            position_data = json.load(position_map)
            position_data.append({JSON_LEAF_ID: -config.get_random_leaf_id(), JSON_DATA_ID: data_id})
            position_map.seek(0)
            json.dump(position_data, position_map, indent=2, sort_keys=True)
            position_map.truncate()

    def delete_data_ids(self, data_ids):
        copy_data_ids = list(data_ids)
        with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.READ_WRITE_MODE) as position_map:
            position_data = json.load(position_map)
            for entry in list(position_data):
                if entry[JSON_DATA_ID] in data_ids:
                    position_data.remove(entry)
                    copy_data_ids.remove(entry[JSON_DATA_ID])
                    if not copy_data_ids:
                        # stop iterating when all data ids are deleted
                        break
            position_map.seek(0)
            json.dump(position_data, position_map, indent=2, sort_keys=True)
            position_map.truncate()

    def get_leaf_ids(self, data_ids):
        copy_data_ids = list(data_ids)
        leaf_ids = []
        with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.READ_MODE) as position_map:
            position_data = json.load(position_map)
            for entry in position_data:
                if entry[JSON_DATA_ID] in data_ids:
                    leaf_ids.append((entry[JSON_DATA_ID], entry[JSON_LEAF_ID]))
                    copy_data_ids.remove(entry[JSON_DATA_ID])
                    if not copy_data_ids:
                        # stop iterating when all leaf ids are found
                        break
            return leaf_ids

    def get_leaf_id(self, data_id):
        with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.READ_MODE) as position_map:
            position_data = json.load(position_map)
            for entry in position_data:
                if entry[JSON_DATA_ID] == data_id:
                    return entry[JSON_LEAF_ID]

    def update_leaf_id(self, data_id, is_in_cloud):
        with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.READ_WRITE_MODE) as position_map:
            position_data = json.load(position_map)
            for entry in position_data:
                if entry[JSON_DATA_ID] == data_id:
                    if is_in_cloud:
                        entry[JSON_LEAF_ID] = abs(entry[JSON_LEAF_ID])
                    else:
                        entry[JSON_LEAF_ID] = -entry[JSON_LEAF_ID]
                    break
            position_map.seek(0)
            json.dump(position_data, position_map, indent=2, sort_keys=True)
            position_map.truncate()

    def choose_new_leaf_id(self, data_id):
        with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.READ_WRITE_MODE) as position_map:
            position_data = json.load(position_map)
            for entry in position_data:
                if entry[JSON_DATA_ID] == data_id:
                    entry[JSON_LEAF_ID] = -config.get_random_leaf_id()
                    break
            position_map.seek(0)
            json.dump(position_data, position_map, indent=2, sort_keys=True)
            position_map.truncate()

    def data_id_exist(self, data_id):
        with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.READ_MODE) as position_map:
            position_data = json.load(position_map)
            for entry in position_data:
                if entry[JSON_DATA_ID] == data_id:
                    return True
            return False

    def count_data_ids(self):
        with data.open_data_file(utils.POSITION_MAP_FILE_NAME, utils.READ_MODE) as position_map:
            position_data = json.load(position_map)
            return len(position_data)
