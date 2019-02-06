"""
@file test_fuel_addons.py

Unit tests to test functionality of adding a fuel scoop and processors to a ship
"""
import pytest
from shipyard.models.spacecraft import Spacecraft


def test_scoop():
    """
    Handles testing adding and removing a single fuel scoop to a ship
    """
    spacecraft = Spacecraft(100)
    assert spacecraft.cost_total == 2.0
    assert spacecraft.tonnage == 100
    assert spacecraft.fuel_scoops == 0

    spacecraft.add_fuel_addons("Fuel Scoop")
    assert spacecraft.cost_total == 3.0
    assert spacecraft.fuel_scoops == 1
    assert spacecraft.tonnage == 100

    spacecraft.remove_fuel_addon("Fuel Scoop")
    assert spacecraft.cost_total == 2.0
    assert spacecraft.fuel_scoops == 0
    assert spacecraft.tonnage == 100


def test_processor():
    """
    Handles adding and removing a single fuel processor to a ship
    """
    spacecraft = Spacecraft(100)
    assert spacecraft.cost_total == 2.0
    assert spacecraft.tonnage == 100
    assert spacecraft.fuel_refine_rate == 0

    spacecraft.add_fuel_addons("Fuel Processor")
    assert spacecraft.cost_total == 2.05
    assert spacecraft.fuel_refine_rate == 20
    assert spacecraft.tonnage == 101

    spacecraft.remove_fuel_addon("Fuel Processor")
    assert spacecraft.cost_total == 2.0
    assert spacecraft.fuel_refine_rate == 0
    assert spacecraft.tonnage == 100

