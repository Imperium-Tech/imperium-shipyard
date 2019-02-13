"""
@file screens.py

Represents a Screen object installed on a ship
"""
from shipyard.models.json_reader import get_file_data


class Screen:
    def __init__(self, name):
        data = get_file_data("hull_screens.json").get(name)

        self.name           = name
        self.tl             = data.get("tl")
        self.tonnage        = data.get("tonnage")
        self.cost           = data.get("cost")
        self.mod_additional = data.get("mod_additional")

