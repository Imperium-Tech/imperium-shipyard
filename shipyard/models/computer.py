"""
@file computer.py

Represents the computers put within a ship and the benefits that come with it
"""
from shipyard.models.json_reader import get_file_data


class Computer:
    def __init__(self, name):
        data = get_file_data("hull_computer.json").get(name)

        self.tl         = data.get("tl")
        self.rating     = data.get("rating")
        self.cost       = data.get("cost")
        self.addons     = list()

    def add_addon(self, name):
        addon = get_file_data("hull_computer.json").get(name)

        if addon.get("rating_increase") is not None:
            self.rating += addon.get("rating_increase")
        self.cost += (addon.get("cost_increase") * self.cost)

        self.addons.append(addon)


