import data
from pyoram import utils

FILE_NAME = 'data%d.oram'


class Stash:
    def __init__(self):
        if not data.is_folder(utils.STASH_FOLDER_NAME):
            data.create_folder(utils.STASH_FOLDER_NAME)

    def add_file(self, data_id, main_part):
        with data.open_data_file_in_stash(FILE_NAME % data_id, utils.WRITE_MODE) as data_item:
            data_item.write(main_part)
        print('add file')

    def remove_file(self):
        print('remove file')
