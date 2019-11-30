"""
@file computer.py

Represents the computers put within a ship and the benefits that come with it
"""
from imperium.models.json_reader import get_file_data


class Computer:
    def __init__(self, name):
        data = get_file_data("hull_computer.json").get(name)

        self.model      = name
        self.tl         = data.get("tl")
        self.rating     = data.get("rating")
        self.cost       = data.get("cost")
        self.bis        = False                 # whether Jump Control Specialization is added
        self.fib        = False                 # whether EMP hardened is added

    def modify_addon(self, name):
        if name == "Jump Control Spec":
            self.bis ^= True
        elif name == "Hardened System":
            self.fib ^= True

    def get_cost(self):
        cost = 0
        cost += self.cost

        if self.bis and self.fib:
            cost += self.cost
        elif self.bis or self.fib:
            cost += self.cost * 0.5

        return cost
