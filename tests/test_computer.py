"""
@file test_computer.py

Unit tests for testing functionality of adding and replacing a computer system in a ship
"""
import pytest
from shipyard.models.computer import Computer
from shipyard.models.spacecraft import Spacecraft


def test_init():
    # Initializing a computer and adding a mod to it, testing the end values
    computer = Computer("model_5")
    assert computer.rating == 25
    assert computer.tl == 13
    assert computer.cost == 10.0

    computer.add_addon("Jump Control Specialisation")
    assert computer.rating == 30
    assert computer.cost == 15.0


def test_adding():
    # Initializing a ship and adding a computer system to it, checking for correct values
    ship = Spacecraft(100)
    assert ship.cost_total == 2.0

    computer = Computer("model_3")
    ship.add_computer(computer)
    assert ship.cost_total == 4.0

