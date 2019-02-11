"""
@file test_screens.py

Unit tests for Screen objects within a ship
"""
import pytest
from shipyard.models.screens import Screen
from shipyard.models.spacecraft import Spacecraft


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
    assert ship.cargo == 200
    assert ship.cost_total == 8.0

    ship.add_screen(damper)
    assert ship.cargo == 150
    assert ship.cost_total == 58.0

    ship.add_screen(meson)
    assert ship.cargo == 100
    assert ship.cost_total == 118.0

    ship.add_screen(extra)
    assert ship.cargo == 100
    assert ship.cost_total == 118.0


def test_removing():
    # Tests removing a screen object from the ship
    ship = Spacecraft(200)
    assert ship.cargo == 200
    assert ship.cost_total == 8.0

    damper = Screen("Nuclear Damper")
    ship.add_screen(damper)
    assert ship.cargo == 150
    assert ship.cost_total == 58.0

    ship.remove_screen(damper)
    assert ship.cargo == 200
    assert ship.cost_total == 8.0

