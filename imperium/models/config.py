"""
@file config.py
@author qu-gg

Class to represent a hull armor configuration
"""
from imperium.models.json_reader import get_file_data


class Config:
    def __init__(self, type):
        data = get_file_data("hull_config.json").get(type)

        self.type               = type
        self.mod_hull_cost      = data.get("mod_hull_cost")
        self.mod_additional     = data.get("mod_additional")
