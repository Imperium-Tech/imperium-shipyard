"""
@file test_software.py

Unit tests for testing functionality of adding and removing software from a ship
"""
import pytest
from shipyard.models.software import Software
from shipyard.models.spacecraft import Spacecraft
from shipyard.models.computer import Computer


def test_init():
    # Testing initialization of different software types
    fire_control = Software("Fire Control", 4)
    assert fire_control.tl == 12
    assert fire_control.rating == 20
    assert fire_control.cost == 8.0

    invalid = Software("Library", 4)
    print(invalid)

    jump_control = Software("Jump Control", 1)
    assert jump_control.tl == 9
    assert jump_control.rating == 5
    assert jump_control.cost == 0.1


def test_adding():
    # Testing adding a single piece of software to a ship
    ship = Spacecraft(100)
    computer = Computer("model_3")
    jump = Software("Jump Control", 2)

    ship.add_computer(computer)
    assert ship.cost_total == 4.0

    ship.add_software(jump)
    assert ship.cost_total == 4.2
    assert ship.software_rating == 10
    assert len(ship.software) == 1

