"""
@file misc.py

Misc class that represents miscellaneous items that don't need individual classes, such as
staterooms, low berths, fuel scoops, etc
"""
from shipyard.models.json_reader import determine_class


class Misc:
    """
    Represents a miscellaneous object that is applied to a ship
    Repair Drone and Escape Pods have special calculations for tonnage and is scaled accordingly
    """
    def __init__(self, name):
        cls = determine_class(name)
        data= cls.get(name)

        self.name               = name
        self.cost               = data.get("cost")
        self.mod_additional     = data.get("mod_additional")
        self.tonnage            = data.get("tonnage")

        if name == "Repair Drone":
            self.cost           = 0.2
            self.tonnage        = 0.01
        if name == "Escape Pods":
            self.tonnage        = 0.5

