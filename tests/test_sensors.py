"""
@file test_sensors.py

Unit tests to test functionality of sensors objects within a ship
"""
import pytest
from imperium.classes.sensors import Sensor
from imperium.classes.spacecraft import Spacecraft


def test_init():
    # Testing initialization of various sensors
    sensor = Sensor("Standard")
    assert sensor.cost == 0
    assert sensor.tonnage == 0
    assert sensor.sensors_dm == -4
    assert sensor.tl == 8
    assert sensor.equipment is not None

    sensor = Sensor("Basic Military")
    assert sensor.cost == 1
    assert sensor.tonnage == 2
    assert sensor.sensors_dm == 0
    assert sensor.tl == 10
    assert sensor.equipment is not None

    sensor = Sensor("Very Advanced")
    assert sensor.cost == 4
    assert sensor.tonnage == 5
    assert sensor.sensors_dm == 2
    assert sensor.tl == 12
    assert sensor.equipment is not None


def test_add_replace():
    # Testing adding and replacing a sensor system
    ship = Spacecraft(100)
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2.0

    sensor = Sensor("Advanced")

    ship.add_sensors(sensor)
    assert ship.get_remaining_cargo() == 97
    assert ship.get_total_cost() == 4.0
    assert ship.sensors is not None

    sensor = Sensor("Basic Civilian")
    ship.add_sensors(sensor)
    assert ship.get_remaining_cargo() == 99
    assert ship.get_total_cost() == 2.05

