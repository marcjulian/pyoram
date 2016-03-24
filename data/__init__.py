import os

from pyoram import utils

base_dir = os.path.dirname(__file__)
stash_dir = os.path.join(base_dir, utils.STASH_FOLDER_NAME)


def open_data_file(filename, mode):
    return open(os.path.join(base_dir, filename), mode)


def open_data_file_in_stash(filename, mode):
    return open(os.path.join(stash_dir, filename), mode)


def is_file_in_stash(filename):
    return os.path.isfile(os.path.join(stash_dir, filename))


def delete_file_in_stash(filename):
    if os.path.isfile(os.path.join(stash_dir, filename)):
        os.remove(os.path.join(stash_dir, filename))


def get_file_names_from_stash():
    return os.listdir(stash_dir)


def file_exists(filename):
    return os.path.isfile(os.path.join(base_dir, filename))


def is_folder(folder_name):
    return os.path.isdir(os.path.join(base_dir, folder_name))


def create_folder(folder_name):
    os.makedirs(os.path.join(base_dir, folder_name))


def get_stash_size():
    return len([name for name in os.listdir(stash_dir) if os.path.isfile(os.path.join(stash_dir, name))])


def get_log_file_name():
    return os.path.join(base_dir, utils.LOG_FILE_NAME)
