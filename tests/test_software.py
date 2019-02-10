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


def test_downgrading():
    # Testing adding a single piece of software to a ship
    ship = Spacecraft(100)
    computer = Computer("model_3")
    jump = Software("Jump Control", 2)
    downgrade = Software("Jump Control", 1)

    ship.add_computer(computer)
    assert ship.cost_total == 4.0

    # Adding the level 2 jump
    ship.add_software(jump)
    assert ship.cost_total == 4.2
    assert ship.software_rating == 10
    assert len(ship.software) == 1

    # Downgrading to the level 1 jump
    ship.add_software(downgrade)
    assert ship.cost_total == 4.1
    assert ship.software_rating == 5
    assert len(ship.software) == 1


def test_invalid():
    # Testing adding a software too high rating for a computer
    ship = Spacecraft(100)
    computer = Computer("model_3")
    jump = Software("Jump Control", 5)

    ship.add_computer(computer)
    assert ship.cost_total == 4.0

    # Adding the level 2 jump
    ship.add_software(jump)
    assert ship.cost_total == 4.0
    assert ship.software_rating == 0
    assert len(ship.software) == 0


def test_overflow():
    # Testing when trying to install a software above the limit
    ship = Spacecraft(100)
    computer = Computer("model_3")
    jump = Software("Jump Control", 2)
    downgrade = Software("Jump Control", 4)

    ship.add_computer(computer)
    assert ship.cost_total == 4.0

    # Adding the level 2 jump
    ship.add_software(jump)
    assert ship.cost_total == 4.2
    assert ship.software_rating == 10
    assert len(ship.software) == 1

    # Trying to upgrade to the level 4 jump
    ship.add_software(downgrade)
    assert ship.cost_total == 4.2
    assert ship.software_rating == 10
    assert len(ship.software) == 1

