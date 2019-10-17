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

        # Setting up missile dictionary for display
        self.missiles        = dict()
        for mtype in data.get("weapons").get("Missile Rack").get("types").keys():
            self.missiles[mtype] = 0

        self.sandcaster_barrels = 0                                # number of sandcaster barrels on turret

    def get_cost(self):
        cost = 0
        cost += self.cost

        # Adding weapon cost
        for wep in self.weapons:
            if wep is not None:
                cost += wep.get("cost")

        # Adding missile costs
        missile_costs = self.data.get("weapons").get("Missile Rack").get("types")
        for key in self.missiles.keys():
            cost += self.missiles.get(key) * missile_costs.get(key)

        # Adding sandcaster costs
        sand_data = self.data.get("weapons").get("Sandcaster").get("barrel_cost")
        cost += self.sandcaster_barrels * sand_data

        return cost

    def get_tonnage(self):
        tonnage = 0
        tonnage += self.tonnage

        # Get missile tonnages
        for key in self.missiles.keys():
            tonnage += self.missiles.get(key)

        # Get sandcaster tonnages
        tonnage += self.sandcaster_barrels

        return tonnage

    def modify_weapon(self, part, idx):
        if part == "---":
            wep = None
        else:
            wep = self.data.get("weapons").get(part)
        self.weapons[idx] = wep

    def modify_missile_ammo(self, type, num):
        if type in self.missiles.keys():
            self.missiles[type] = num

    def modify_sandcaster_barrel(self, num):
        self.sandcaster_barrels = num
