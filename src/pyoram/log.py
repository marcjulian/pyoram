import logging

import data


def get_logger(name):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(data.get_log_file_name())
    file_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # add formatter to handlers
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
