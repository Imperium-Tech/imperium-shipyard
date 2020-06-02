"""
@file test_screens.py

Unit tests for Screen objects within a ship
"""
import pytest
from imperium.classes.screens import Screen
from imperium.classes.spacecraft import Spacecraft


def test_init():
    # Tests initialization both screen types
    damper = Screen("Nuclear Damper")
    assert damper.tonnage == 50
    assert damper.cost == 50
    assert damper.tl == 12

    meson = Screen("Meson Screen")
    assert meson.tonnage == 50
    assert meson.cost == 60
    assert meson.tl == 12


def test_adding():
    # Tests adding each screen type
    damper = Screen("Nuclear Damper")
    meson = Screen("Meson Screen")
    extra = Screen("Nuclear Damper")

    ship = Spacecraft(200)
    assert ship.get_remaining_cargo() == 200
    assert ship.get_total_cost() == 8.0

    ship.modify_screen(damper)
    assert ship.get_remaining_cargo() == 150
    assert ship.get_total_cost() == 58.0

    ship.modify_screen(meson)
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 118.0


def test_removing():
    # Tests removing a screen object from the ship
    ship = Spacecraft(200)
    assert ship.get_remaining_cargo() == 200
    assert ship.get_total_cost() == 8.0

    damper = Screen("Nuclear Damper")
    ship.modify_screen(damper)
    assert ship.get_remaining_cargo() == 150
    assert ship.get_total_cost() == 58.0

    new_damper = Screen("Nuclear Damper")
    ship.modify_screen(new_damper)
    assert ship.get_remaining_cargo() == 200
    assert ship.get_total_cost() == 8.0

