"""
@file turrets.py

Module that contains classes and relevant data for a turret
"""
from json_reader import get_file_data


class Turret:
    """
    Represents a single turret on a ship

    :param model_type: which type of model the turret is
    """
    def __init__(self, model_type):
        data = get_file_data("hull_turrets.json")

        self.data = data
        self.name = model_type                                # name of the model
        self.model = data.get("models").get(model_type)       # model of the turret
        self.tonnage    = self.model.get("tonnage")           # size of the turret and addons
        self.addons     = list()                              # list of the addons for this turret
        self.max_wep    = self.model.get("num_weapons")       # max number of weapons per turret type
        self.weapons    = list()                              # list of the weapons on this turret
        self.cost       = self.model.get("cost")              # cost of the turret and addons

    def add_addon(self, part):
        # Grabbing addon info from data
        addon = self.data.get("addons").get(part)

        # Appending addon and related costs to turret fields
        self.addons.append(addon)
        self.tonnage += addon.get("tonnage")

        if part == "Pop-up Turret":
            self.cost += addon.get("cost")
        if part == "Fixed Mounting":
            self.cost *= addon.get("cost")

    def add_weapon(self, part):
        # Checks if the turret can have more weapons
        if len(self.weapons) == self.max_wep:
            print("Maximum number of weapons reached for {}: {}/{}".format(self.name, len(self.weapons), self.max_wep))
            return

        # Grabbing weapon info from data
        weapon = self.data.get("weapons").get(part)

        # Appending weapon and related costs to turret fields
        self.weapons.append(weapon)
        self.cost += weapon.get("cost")

    def remove_weapon(self, part):
        # If no weapons are attached, error and return
        if len(self.weapons) == 0:
            print("Error: no weapons to remove.")
            return

        wep = self.data.get("weapons").get(part)

        # Check if any weapon matches this weapon. If none, print error.
        for w in self.weapons:
            if wep == w:
                self.weapons.remove(w)
                break
        print("Error: {} not attached to {}".format(part, self.name))

