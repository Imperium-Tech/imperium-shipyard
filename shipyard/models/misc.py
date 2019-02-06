"""
@file misc.py

Misc class that represents miscellaneous items that don't need individual classes, such as
staterooms, low berths, fuel scoops, etc
"""
from shipyard.models.json_reader import get_file_data
from shipyard.models.json_reader import determine_class

IRREGULAR_LIST = ["Repair Drone", "Escape Pods"]


class Misc:
    def __init__(self, name):
        c = determine_class(name)
        data= c.get(name)

        self.name               = name
        self.cost               = data.get("cost")
        self.mod_additional     = data.get("mod_additional")

        if name in IRREGULAR_LIST:
            self.tonnage        = 0
        else:
            self.tonnage        = data.get("tonnage")
