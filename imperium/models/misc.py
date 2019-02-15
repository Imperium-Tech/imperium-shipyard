"""
@file misc.py

Misc class that represents miscellaneous items that don't need individual classes, such as
staterooms, low berths, fuel scoops, etc
"""
from imperium.models.json_reader import get_file_data


class Misc:
    """
    Represents a miscellaneous object that is applied to a ship
    Repair Drone and Escape Pods have special calculations for tonnage and is scaled accordingly
    """
    def __init__(self, name):
        data = get_file_data("hull_misc.json")
        obj = data.get(name)

        self.name               = name
        self.cost               = obj.get("cost")
        self.mod_additional     = obj.get("mod_additional")
        self.tonnage            = obj.get("tonnage")
