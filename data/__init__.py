import os

base_dir = os.path.dirname(__file__)


def open_data_file(filename, mode):
    return open(os.path.join(base_dir, filename), mode)


def file_exists(filename):
    return os.path.isfile(os.path.join(base_dir, filename))