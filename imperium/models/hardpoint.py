"""
@file hardpoint.py

Represents a single hardpoint on a ship and its contained items/customizations
"""
class Hardpoint:
    def __init__(self):
        self.turret      = None     # turret object

    def add_turret(self, turret):
        self.turret = turret

    def get_cost(self):
        return self.turret.cost

    def get_tonnage(self):
        return self.turret.tonnage