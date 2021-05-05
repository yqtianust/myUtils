import os
from datetime import datetime
import logging


def create_folder(path):
    if not os.path.exists(path):
        print("Creating Dirs: {}".format(path))
        os.makedirs(path)


def get_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    return timestamp


def create_logger(filepath, logger_name=None):
    if logger_name is None:
        logger_name = filepath

    create_folder(os.path.dirname(filepath))
    logging.basicConfig(filename=filepath, filemode='a', level=logging.INFO, datefmt='%m-%d %H:%M:%S',
                        format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(logger_name)
    # logger.addHandler(logging.FileHandler(filepath, 'a'))
    log = logger.info
    return log
