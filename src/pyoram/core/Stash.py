import data
from pyoram import utils

FILE_NAME = 'data%d.oram'


class Stash:
    def __init__(self):
        if not data.is_folder(utils.STASH_FOLDER_NAME):
            data.create_folder(utils.STASH_FOLDER_NAME)

    def get_filename(self, data_id):
        return FILE_NAME % data_id

    def add_file(self, data_id, main_part):
        with data.open_data_file_in_stash(self.get_filename(data_id), utils.WRITE_MODE) as data_item:
            data_item.write(main_part)

    def open_file(self, data_id):
        with data.open_data_file_in_stash(self.get_filename(data_id), utils.READ_MODE) as data_item:
            data_block = data_item.read()
            return data_block

    def delete_data_items(self, data_ids):
        for data_id in data_ids:
            self.delete_data_item(data_id)

    def delete_data_item(self, data_id):
        data.delete_file__in_stash(self.get_filename(data_id))

    def get_data_item(self, data_id):
        if data.is_file_in_stash(self.get_filename(data_id)):
            with data.open_data_file_in_stash(self.get_filename(data_id), utils.READ_MODE) as data_item:
                return data_id, data_item.read()
