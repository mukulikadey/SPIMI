from collections import OrderedDict
from glob import iglob
import json


def generate_index_from_files():
    index = OrderedDict()
    files_paths = []

    for file_path in iglob('DISK/BLOCK*.txt'):
        files_paths.append(file_path)

    for file in files_paths:
        with open(file, 'r') as file:
            block_object = json.load(file)
            index.update(block_object)

    return index