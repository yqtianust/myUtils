import os
from datetime import datetime


def create_folder(path):
    if not os.path.exists(path):
        print("Creating Dirs: {}".format(path))
        os.makedirs(path)


def get_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    return timestamp
