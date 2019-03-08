"""
@file test_bayweapons.py

Unit tests for testing functionality of adding a bayweapon to a ship
"""
import pytest
from imperium.models.armor import Armor
from imperium.models.spacecraft import Spacecraft


def test_init():
    armor = Armor("Titanium Steel")
    assert armor.tl == 7
    assert armor.protection == 2
    assert armor.hull_amount == 0.05
    assert armor.cost_by_hull_percentage == 0.05

    armor = Armor("Crystaliron")
    assert armor.tl == 10
    assert armor.protection == 4
    assert armor.hull_amount == 0.05
    assert armor.cost_by_hull_percentage == 0.20

    armor = Armor("Bonded Superdense")
    assert armor.tl == 14
    assert armor.protection == 6
    assert armor.hull_amount == 0.05
    assert armor.cost_by_hull_percentage == 0.50


def test_add():
    ship = Spacecraft(200)

    armor = Armor("Titanium Steel")
    assert armor.tl == 7
    assert armor.protection == 2
    assert armor.hull_amount == 0.05
    assert armor.cost_by_hull_percentage == 0.05

    ship.add_armor(armor)
    assert ship.cargo == 190
    assert ship.armor_total == 2
    assert ship.cost_total == 18


def test_remove():
    """
    Tests removing a piece of armor from the ship
    """
    ship = Spacecraft(200)

    armor = Armor("Titanium Steel")
    assert armor.tl == 7
    assert armor.protection == 2
    assert armor.hull_amount == 0.05
    assert armor.cost_by_hull_percentage == 0.05

    ship.add_armor(armor)
    assert ship.cargo == 190
    assert ship.armor_total == 2
    assert ship.cost_total == 18

    ship.remove_armor(armor)
    assert ship.cargo == 200
    assert ship.armor_total == 0
    assert ship.cost_total == 8

