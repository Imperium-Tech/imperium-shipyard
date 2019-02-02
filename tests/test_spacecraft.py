"""
test_spacecraft.py

Unit tests for classes in shipyard.models.spacecraft
"""
import pytest
from shipyard.models.spacecraft import Spacecraft
from shipyard.models.turrets import Turret


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
