"""
@file test_screens.py

Unit tests for Screen objects within a ship
"""
import pytest
from imperium.models.screens import Screen
from imperium.models.spacecraft import Spacecraft


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
    # Tests adding each screen type and tests the ship checks for duplicates
    damper = Screen("Nuclear Damper")
    meson = Screen("Meson Screen")
    extra = Screen("Nuclear Damper")

    ship = Spacecraft(200)
    assert ship.get_remaining_cargo() == 200
    assert ship.get_total_cost() == 8.0

    ship.add_screen(damper)
    assert ship.get_remaining_cargo() == 150
    assert ship.get_total_cost() == 58.0

    ship.add_screen(meson)
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 118.0

    ship.add_screen(extra)
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 118.0


def test_removing():
    # Tests removing a screen object from the ship
    ship = Spacecraft(200)
    assert ship.get_remaining_cargo() == 200
    assert ship.get_total_cost() == 8.0

    damper = Screen("Nuclear Damper")
    ship.add_screen(damper)
    assert ship.get_remaining_cargo() == 150
    assert ship.get_total_cost() == 58.0

    ship.remove_screen(damper)
    assert ship.get_remaining_cargo() == 200
    assert ship.get_total_cost() == 8.0

