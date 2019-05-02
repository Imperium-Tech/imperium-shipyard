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
    fuel_scoop = Misc("Fuel Scoop")
    assert fuel_scoop.tonnage == 0
    assert fuel_scoop.cost == 1.0

    stateroom = Misc("Stateroom")
    assert stateroom.tonnage == 4.0
    assert stateroom.cost == 0.5

    escape_pod = Misc("Escape Pods")
    assert escape_pod.tonnage == 0.5
    assert escape_pod.cost == 0.1

    repair_drone = Misc("Repair Drone")
    assert repair_drone.tonnage == 0.01
    assert repair_drone.cost == 0.2


def test_normal_add():
    ship = Spacecraft(100)

    # Adding and removing a Fuel Scoop
    fuel_scoop = Misc("Fuel Scoop")
    ship.add_misc(fuel_scoop)
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 3
    ship.remove_misc(fuel_scoop)


def test_escape_pods():
    ship = Spacecraft(100)

    # Adding a stateroom then an escape pod
    stateroom = Misc("Stateroom")
    ship.add_misc(stateroom)
    assert ship.get_remaining_cargo() == 96
    assert ship.get_total_cost() == 2.5

    escape_pod = Misc("Escape Pods")
    ship.add_misc(escape_pod)
    assert ship.get_remaining_cargo() == 95.5
    assert ship.get_total_cost() == 2.6


def test_repair_drones():
    ship = Spacecraft(100)

    # Adding repair drones and checking dynamic costs
    repair_drones = Misc("Repair Drone")
    ship.add_misc(repair_drones)
    assert ship.get_remaining_cargo() == 99
    assert ship.get_total_cost() == 2.2

    # Removing the drone
    ship.remove_misc(repair_drones)
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2.0

