import data
from pyoram import utils


class Stash:
    def __init__(self):
        if not data.is_folder(utils.STASH_FOLDER_NAME):
            data.create_folder(utils.STASH_FOLDER_NAME)

    def add_file(self):
        print('add file')

    def remove_file(self):
        print('remove file')
