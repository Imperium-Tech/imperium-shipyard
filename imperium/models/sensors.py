"""
@file sensors.py

Represents a Sensor object installed on a ship
"""
from imperium.models.json_reader import get_file_data


class Sensor:
    def __init__(self, name):
        data = get_file_data("hull_sensors.json").get(name)

        self.tl             = data.get("tl")
        self.equipment      = data.get("equipment")
        self.tonnage        = data.get("tonnage")
        self.cost           = data.get("cost")
        self.sensors_dm     = data.get("sensors_dm")

