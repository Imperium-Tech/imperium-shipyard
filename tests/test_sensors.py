"""
@file test_sensors.py

Unit tests to test functionality of sensors objects within a ship
"""
import pytest
from shipyard.models.sensors import Sensor
from shipyard.models.spacecraft import Spacecraft


def test_init():
    # Testing initialization of various sensors
    sensor = Sensor("standard")
    assert sensor.cost == 0
    assert sensor.tonnage == 0
    assert sensor.sensors_dm == -4
    assert sensor.tl == 8
    assert sensor.equipment is not None

    sensor = Sensor("basic_military")
    assert sensor.cost == 1
    assert sensor.tonnage == 2
    assert sensor.sensors_dm == 0
    assert sensor.tl == 10
    assert sensor.equipment is not None

    sensor = Sensor("very_advanced")
    assert sensor.cost == 4
    assert sensor.tonnage == 5
    assert sensor.sensors_dm == 2
    assert sensor.tl == 12
    assert sensor.equipment is not None


def test_add_replace():
    # Testing adding and replacing a sensor system
    ship = Spacecraft(100)
    assert ship.cargo == 100
    assert ship.cost_total == 2.0

    sensor = Sensor("advanced")

    ship.add_sensors(sensor)
    assert ship.cargo == 97
    assert ship.cost_total == 4.0
    assert ship.sensors is not None

    sensor = Sensor("basic_civilian")
    ship.add_sensors(sensor)
    assert ship.cargo == 99
    assert ship.cost_total == 2.05

