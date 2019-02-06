"""
@file misc.py

Misc class that represents miscellaneous items that don't need individual classes, such as
staterooms, low berths, fuel scoops, etc
"""
from shipyard.models.json_reader import get_file_data

IRREGULAR_LIST = ["Repair Drone", "Escape Pods"]


class Misc:
    def __init__(self, name):
        data = get_file_data(name)
        self.name               = name
        self.cost               = data.get("cost")
        self.mod_additional     = data.get("mod_additional")

        if name in IRREGULAR_LIST:
            self.tonnage        = None
        else:
            self.tonnage        = data.get("tonnage")
