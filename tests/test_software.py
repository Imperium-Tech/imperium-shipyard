"""
@file test_software.py

Unit tests for testing functionality of adding and removing software from a ship
"""
import pytest
from shipyard.models.software import Software
from shipyard.models.spacecraft import Spacecraft


def test_init():
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

