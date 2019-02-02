"""
pplant.py

Contains classes for the power plant
"""
from shipyard.models.json_reader import get_file_data


class PPlant:
    """
    The P-Plant, or Power Plant, in a spaceship
    
    :param plant_type: The type of P-Plant by letter
    """
    def __init__(self, plant_type):
        self.plant_type     = None  # the drive designation (A, F, H, etc.)
        self.tonnage        = 0     # the size of the drive in tons
        self.cost           = 0     # the cost of the drive
        self.fuel_two_weeks = 0     # fuel consumption every 2 weeks

        # set drive type from init
        self.plant_type = plant_type

        # grab additional info from json
        data = get_file_data(pplant_data.json)
        plant_item = data.get(plant_type)

        # set determined object state
        self.tonnage = plant_item.get("tonnage")
        self.cost = plant_item.get("cost")
        self.fuel_two_weeks = plant_item.get("fuel_two_weeks")
