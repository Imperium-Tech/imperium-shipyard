"""
@file test_fuel_addons.py

Unit tests to test functionality of adding a fuel scoop and processors to a ship
"""
import pytest
from imperium.models.spacecraft import Spacecraft
from imperium.models.misc import Misc


def test_init():
    """
    Testing initialization of various Misc objects
    """
    stateroom = Misc("Staterooms", 1)
    assert stateroom.tonnage == 4.0
    assert stateroom.cost == 0.5

    escape_pod = Misc("Escape Pods", 1)
    assert escape_pod.tonnage == 0.5
    assert escape_pod.cost == 0.1

    repair_drone = Misc("Repair Drones", 1)
    assert repair_drone.tonnage == 0.01
    assert repair_drone.cost == 0.2


def test_normal_add():
    ship = Spacecraft(100)

    # Adding and removing a Fuel Processor
    fuel_processor = Misc("Fuel Processors", 1)
    ship.modify_misc(fuel_processor)
    assert ship.get_remaining_cargo() == 99
    assert ship.get_total_cost() == 2.05
    ship.remove_misc("Fuel Processors")
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2.0


def test_escape_pods():
    ship = Spacecraft(100)

    # Adding a stateroom then an escape pod
    stateroom = Misc("Staterooms", 1)
    ship.modify_misc(stateroom)
    assert ship.get_remaining_cargo() == 96
    assert ship.get_total_cost() == 2.5

    escape_pod = Misc("Escape Pods", 1)
    ship.modify_misc(escape_pod)
    assert ship.get_remaining_cargo() == 95.5
    assert ship.get_total_cost() == 2.6


def test_repair_drones():
    ship = Spacecraft(100)

    # Adding repair drones and checking dynamic costs
    repair_drones = Misc("Repair Drones", 1)
    ship.modify_misc(repair_drones)
    assert ship.get_remaining_cargo() == 99.0
    assert ship.get_total_cost() == 2.2

    # Removing the drone
    ship.remove_misc("Repair Drones")
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2.0


def test_swap():
    ship = Spacecraft(100)

    # Adding repair drones and checking dynamic costs
    repair_drones = Misc("Repair Drones", 1)
    ship.modify_misc(repair_drones)
    assert ship.get_remaining_cargo() == 99.0
    assert ship.get_total_cost() == 2.2

    # Swapping for more drones
    repair_drones = Misc("Repair Drones", 2)
    ship.modify_misc(repair_drones)
    assert ship.get_remaining_cargo() == 98.0
    assert ship.get_total_cost() == 2.4
