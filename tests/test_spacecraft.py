"""
test_spacecraft.py

Unit tests for classes in shipyard.models.spacecraft
"""
import pytest

from imperium.classes.config import Config
from imperium.classes.hardpoint import Hardpoint
from imperium.classes.spacecraft import Spacecraft
from imperium.classes.turrets import Turret
from imperium.classes.armour import Armour


def test_spacecraft_init():
    """
    Tests the initialization of a new Spacecraft (hull)
    """
    spacecraft = Spacecraft(1000)
    assert spacecraft.tonnage == 1000
    assert spacecraft.get_remaining_cargo() == 1000
    assert spacecraft.hull_hp == 1000 // 50
    assert spacecraft.structure_hp == 1000 // 50
    assert spacecraft.fuel_max == 0
    assert spacecraft.armour_total == 0
    assert spacecraft.hull_type.type == "Standard"
    assert spacecraft.hull_designation == "B"


def test_turret_functionality():
    """
    Tests the functionality of adding and removing a turret from a ship
    """
    ship = Spacecraft(100)

    # Turret init with a wep and addon
    hardpoint = Hardpoint("1")
    turret = Turret("Single Turret")
    hardpoint.add_turret(turret)
    turret.modify_weapon("Beam Laser", 0)

    # Adding and removing the turret, checking ship specs
    ship.add_hardpoint(hardpoint)
    assert ship.get_remaining_cargo() == 99
    assert ship.get_total_cost() == 3.2

    turret.modify_weapon("---", 0)
    assert ship.get_remaining_cargo() == 99
    assert ship.get_total_cost() == 2.2


def test_set_tonnage():
    """
    Tests functionality of setting tonnage and the updates that comes with that
    """
    ship = Spacecraft(100)
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2.0
    assert ship.tonnage == 100
    assert ship.structure_hp == 2
    assert ship.hull_hp == 2
    assert ship.armour_total == 0

    ship.set_tonnage(200)
    assert ship.get_remaining_cargo() == 200
    assert ship.get_total_cost() == 8.0
    assert ship.tonnage == 200
    assert ship.structure_hp == 4
    assert ship.hull_hp == 4
    assert ship.armour_total == 0

    armour = Armour("Titanium Steel")
    ship.add_armour(armour)
    assert ship.get_remaining_cargo() == 190
    assert ship.get_total_cost() == 8.4
    assert ship.tonnage == 200
    assert ship.structure_hp == 4
    assert ship.hull_hp == 4
    assert ship.armour_total == 2

    ship.set_tonnage(100)
    assert ship.get_remaining_cargo() == 95
    assert ship.get_total_cost() == 2.1
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
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2.0
    assert ship.tonnage == 100
    assert ship.hull_type.type == "Standard"

    config = Config("Streamlined")
    ship.edit_hull_config(config)
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2.2
    assert ship.tonnage == 100
    assert ship.hull_type.type == "Streamlined"

    config = Config("Standard")
    ship.edit_hull_config(config)
    ship.set_tonnage(100)
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2.0
    assert ship.tonnage == 100
    assert ship.hull_type.type == "Standard"


def test_fuel_add():
    ship = Spacecraft(100)
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 100
    assert ship.fuel_max == 0

    ship.set_fuel(50)
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 50
    assert ship.fuel_max == 50


def test_lowest_drive():
    ship = Spacecraft(100)
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 100

    drive = ship.get_lowest_drive()
    assert drive == "A"


def test_fuel_scoop():
    ship = Spacecraft(100)
    assert ship.hull_type.type == "Standard"
    assert ship.fuel_scoop is False
    assert ship.get_total_cost() == 2.0

    ship.modify_fuel_scoops()
    assert ship.hull_type.type == "Standard"
    assert ship.fuel_scoop is True
    assert ship.get_total_cost() == 3.0

