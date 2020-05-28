"""
@file software.py

Class that represents a piece of software and its level for a ship
"""
from imperium.classes.json_reader import get_file_data


class Software:
    def __init__(self, name, level):
        data = get_file_data("hull_software.json").get(name)
        software = data.get(str(level))

        if software is None:
            print("Error: invalid software level for {}".format(name))
            return

        self.type               = name
        self.level              = level
        self.tl                 = software.get("tl")
        self.rating             = software.get("rating")
        self.cost               = software.get("cost")
        self.mod_additional     = data.get("mod_additional")
