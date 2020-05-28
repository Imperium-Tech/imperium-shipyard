"""
@file hardpoint.py

Represents a single hardpoint on a ship and its contained items/customizations
"""
from imperium.classes.json_reader import get_file_data


class Hardpoint:
    def __init__(self, id):
        self.data = get_file_data("hull_turrets.json")
        self.id          = id       # hardpoint id
        self.turret      = None     # turret object
        self.popup       = False
        self.fixed       = False

    def modify_addon(self, part):
        """
        Handles adding an add-on to the turret
        :param part: Name of the add-on to add
        """
        if part == "Pop-up Turret":
            self.popup ^= True
        if part == "Fixed Mounting":
            self.fixed ^= True

    def add_turret(self, turret):
        # Modifying/adding turret of a hardpoint
        self.turret = turret
        if self.turret is not None and self.turret.name == "Bay Weapon":
            self.popup = False
            self.fixed = False

    def get_cost(self):
        """
        Handles getting the total cost of a hardpoint and its options
        :return: cost
        """
        cost = 0

        if self.turret is not None:
            cost += self.turret.get_cost()
        if self.popup is True:
            cost += 1.0
        if self.fixed is True:
            cost *= 0.5

        return cost

    def get_tonnage(self):
        """
        Handles getting the total tonnage of a hardpoint and its options
        :return: tonnage
        """
        tonnage = 0

        if self.turret is not None:
            tonnage += self.turret.get_tonnage()
        if self.popup is True:
            tonnage += 2.0

        return tonnage
