"""
test_spacecraft.py

Unit tests for classes in shipyard.models.spacecraft
"""
import pytest

from imperium.models.config import Config
from imperium.models.spacecraft import Spacecraft
from imperium.models.turrets import Turret
from imperium.models.armour import Armour


def test_spacecraft_init():
    """
    Tests the initialization of a new Spacecraft (hull)
    """
    spacecraft = Spacecraft(1000)
    assert spacecraft.tonnage == 1000
    assert spacecraft.cargo == 1000
    assert spacecraft.hull_hp == 1000 // 50
    assert spacecraft.structure_hp == 1000 // 50
    assert spacecraft.cost_hull == 100
    assert spacecraft.cost_total == 100
    assert spacecraft.fuel_max == 0
    assert spacecraft.armour_total == 0
    assert spacecraft.hull_type == "Standard"
    assert spacecraft.hull_designation == "B"


def test_turret_functionality():
    """
    Tests the functionality of adding and removing a turret from a ship
    """
    ship = Spacecraft(100)

    # Turret init with a wep and addon
    turret = Turret("Single Turret")
    turret.add_weapon("Beam Laser")
    turret.add_addon("Pop-up Turret")

    # Adding and removing the turret, checking ship specs
    ship.add_turret(turret)
    assert ship.cargo == 97
    assert ship.cost_total == 4.2
    assert len(ship.turrets) == 1

    ship.remove_turret(0)
    assert ship.cargo == 100
    assert ship.cost_total == 2.0
    assert len(ship.turrets) == 0


def test_set_tonnage():
    """
    Tests functionality of setting tonnage and the updates that comes with that
    """
    ship = Spacecraft(100)
    assert ship.cargo == 100
    assert ship.cost_total == 2.0
    assert ship.tonnage == 100
    assert ship.structure_hp == 2
    assert ship.hull_hp == 2
    assert ship.armour_total == 0

    ship.set_tonnage(200)
    assert ship.cargo == 200
    assert ship.cost_total == 8.0
    assert ship.tonnage == 200
    assert ship.structure_hp == 4
    assert ship.hull_hp == 4
    assert ship.armour_total == 0

    armour = Armour("Titanium Steel")
    ship.add_armour(armour)
    assert ship.cargo == 190
    assert ship.cost_total == 18
    assert ship.tonnage == 200
    assert ship.structure_hp == 4
    assert ship.hull_hp == 4
    assert ship.armour_total == 2

    ship.set_tonnage(100)
    assert ship.cargo == 95
    assert ship.cost_total == 7
    assert ship.tonnage == 100
    assert ship.armour_total == 2
    assert ship.structure_hp == 2
    assert ship.hull_hp == 2


def test_config_functionality():
    """
    Tests functionality for adding configurations and swapping tonnage values
    :return:
    """
    ship = Spacecraft(100)
    assert ship.cargo == 100
    assert ship.cost_total == 2.0
    assert ship.tonnage == 100
    assert ship.cost_hull == 2.0
    assert ship.base_cost_hull == 2.0
    assert ship.hull_type == "Standard"

    config = Config("Streamlined")
    ship.edit_hull_config(config)
    assert ship.cargo == 100
    assert ship.cost_total == 2.2
    assert ship.tonnage == 100
    assert ship.cost_hull == 2.2
    assert ship.base_cost_hull == 2.0
    assert ship.hull_type == "Streamlined"

    config = Config("Standard")
    ship.edit_hull_config(config)
    ship.set_tonnage(100)
    assert ship.cargo == 100
    assert ship.cost_total == 2.0
    assert ship.tonnage == 100
    assert ship.cost_hull == 2.0
    assert ship.base_cost_hull == 2.0
    assert ship.hull_type == "Standard"


def test_fuel_add():
    ship = Spacecraft(100)
    assert ship.tonnage == 100
    assert ship.cargo == 100
    assert ship.fuel_max == 0

    ship.set_fuel(50)
    assert ship.tonnage == 100
    assert ship.cargo == 50
    assert ship.fuel_max == 50

