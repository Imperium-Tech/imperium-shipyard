"""
@file option.py
@author qu-gg

Class to represent a hull option configuration
"""
from imperium.classes.json_reader import get_file_data


class Option:
    def __init__(self, name):
        data = get_file_data("hull_options.json").get(name)

        self.name               = name
        self.cost_per_hull_ton  = data.get("cost_per_hull_ton")
