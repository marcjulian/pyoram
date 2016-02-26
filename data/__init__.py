import os

from pyoram import utils

base_dir = os.path.dirname(__file__)


def open_data_file(filename, mode):
    return open(os.path.join(base_dir, filename), mode)


def open_data_file_in_stash(filename, mode):
    return open(os.path.join(os.path.join(base_dir, utils.STASH_FOLDER_NAME), filename), mode)


def file_exists(filename):
    return os.path.isfile(os.path.join(base_dir, filename))


def is_folder(folder_name):
    return os.path.isdir(os.path.join(base_dir, folder_name))


def create_folder(folder_name):
    os.makedirs(os.path.join(base_dir, folder_name))
