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
    :param name: represents the name of the object, found within hull_misc.json
    :param num: represents the number of that object, multiples tonnage and cost
    """
    def __init__(self, name, num):
        data = get_file_data("hull_misc.json")
        obj = data.get(name)

        self.name               = name
        self.num                = num
        self.cost = obj.get("cost") * num
        self.mod_additional = obj.get("mod_additional")
        self.tonnage = obj.get("tonnage") * num
