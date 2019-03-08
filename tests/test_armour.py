"""
@file test_armour.py

Unit tests for testing functionality of adding armor pieces to a ship
"""
import pytest
from imperium.models.armour import Armour
from imperium.models.spacecraft import Spacecraft


def test_init():
    """
    Tests initializing all types of armour
    """
    armour = Armour("Titanium Steel")
    assert armour.tl == 7
    assert armour.protection == 2
    assert armour.hull_amount == 0.05
    assert armour.cost_by_hull_percentage == 0.05

    armour = Armour("Crystaliron")
    assert armour.tl == 10
    assert armour.protection == 4
    assert armour.hull_amount == 0.05
    assert armour.cost_by_hull_percentage == 0.20

    armour = Armour("Bonded Superdense")
    assert armour.tl == 14
    assert armour.protection == 6
    assert armour.hull_amount == 0.05
    assert armour.cost_by_hull_percentage == 0.50


def test_add():
    """
    Tests adding a piece of armour to a ship
    """
    ship = Spacecraft(200)

    armour = Armour("Titanium Steel")
    assert armour.tl == 7
    assert armour.protection == 2
    assert armour.hull_amount == 0.05
    assert armour.cost_by_hull_percentage == 0.05

    ship.add_armour(armour)
    assert ship.cargo == 190
    assert ship.armour_total == 2
    assert ship.cost_total == 18


def test_remove():
    """
    Tests removing a piece of armour from the ship
    """
    ship = Spacecraft(200)

    armour = Armour("Titanium Steel")
    assert armour.tl == 7
    assert armour.protection == 2
    assert armour.hull_amount == 0.05
    assert armour.cost_by_hull_percentage == 0.05

    ship.add_armour(armour)
    assert ship.cargo == 190
    assert ship.armour_total == 2
    assert ship.cost_total == 18

    ship.remove_armour(armour)
    assert ship.cargo == 200
    assert ship.armour_total == 0
    assert ship.cost_total == 8

    # testing for removing a non-attached armour piece
    ship.remove_armour(armour)
    assert ship.cargo == 200
    assert ship.armour_total == 0
    assert ship.cost_total == 8


def test_swap():
    """
    Tests swapping the tonnage on the ship and making sure the ship's values
    translate accordingly
    """
    ship = Spacecraft(200)

    armour = Armour("Titanium Steel")
    assert armour.tl == 7
    assert armour.protection == 2
    assert armour.hull_amount == 0.05
    assert armour.cost_by_hull_percentage == 0.05

    ship.add_armour(armour)
    assert ship.cargo == 190
    assert ship.armour_total == 2
    assert ship.cost_total == 18

    ship.set_tonnage(100)
    assert ship.cargo == 95
    assert ship.armour_total == 2
    assert ship.cost_total == 7

    ship.remove_armour(armour)
    assert ship.cargo == 100
    assert ship.armour_total == 0
    assert ship.cost_total == 2

