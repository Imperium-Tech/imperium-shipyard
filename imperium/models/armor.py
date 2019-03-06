"""
@file armor.py

Represents a piece of armor that can be added onto a ship
"""
from imperium.models.json_reader import get_file_data


class Armor:
    def __init__(self, type):
        data = get_file_data("hull_armor.json").get(type)

        self.type                       = type
        self.tl                         = data.get("tl")
        self.protection                 = data.get("protection")
        self.hull_amount                = data.get("hull_amount")
        self.cost_by_hull_percentage    = data.get("cost_by_hull_percentage")
