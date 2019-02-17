"""
@file bayweapon.py

Class that represents a Bay weapon for a ship
"""
from imperium.models.json_reader import get_file_data


class Bayweapon:
    def __init__(self, name):
        data = get_file_data("hull_bayweapon.json").get(name)

        self.name           = name
        self.tl             = data.get("tl")
        self.range          = data.get("range")
        self.damage         = data.get("damage")
        self.cost           = data.get("cost")
        self.tonnage        = 51
        self.mod_additional = data.get("mod_additional")
