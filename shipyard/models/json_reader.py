"""
json_reader.py

Provides json file from the resources directory
"""
import json
import os.path


def get_file_data(filename):
    """
    get_file_data

    :param filename: The name of the file to get
    """
    data = None
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../resources/" + filename)
    with open(path) as f:
        data = json.load(f)

    return data