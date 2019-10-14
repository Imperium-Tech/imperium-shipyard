"""
@file turrets.py

Module that contains classes and relevant data for a turret
"""
from imperium.models.json_reader import get_file_data


class Turret:
    """
    Represents a single turret on a ship

    :param model_type: which type of model the turret is
    """
    def __init__(self, model_type):
        data = get_file_data("hull_turrets.json")

        self.data            = data
        self.name            = model_type                          # name of the model
        self.model           = data.get("models").get(model_type)  # model of the turret
        self.tonnage         = self.model.get("tonnage")           # size of the turret and addons
        self.max_wep         = self.model.get("num_weapons")       # max number of weapons per turret type
        self.weapons         = [None for _ in range(self.max_wep)] # list of the weapons on this turret
        self.cost            = self.model.get("cost")              # cost of the turret and addons

    def get_cost(self):
        cost = 0
        cost += self.cost
        for wep in self.weapons:
            if wep is not None:
                cost += wep.get("cost")
        return cost

    def modify_weapon(self, part, idx):
        if part == "---":
            wep = None
        else:
            wep = self.data.get("weapons").get(part)
        self.weapons[idx] = wep
