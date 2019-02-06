"""
json_reader.py

Provides json file from the resources directory
"""
import json
import os.path


def get_file_data(filename):
    """
    Parses the filename given, grabs the corresponding .json file, and converts it into a
    Python-usable dictionary
    :param filename: The name of the file to get
    :return: Dictionary of the converted .json file
    """
    data = None
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../resources/" + filename)
    with open(path) as f:
        data = json.load(f)

    return data


def determine_class(name):
    """
    Determines which of the .json classes a specific object name belongs to
    :param name: Name of the object to find
    """
    for file in os.listdir("../resources"):
        f = open("../resources/{}".format(file))
        data = json.load(f)
        if name in data.keys():
            return data
