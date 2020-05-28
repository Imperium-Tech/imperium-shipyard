"""
@file test_software.py

Unit tests for testing functionality of adding and removing software from a ship
"""
import pytest
from imperium.classes.software import Software
from imperium.classes.spacecraft import Spacecraft
from imperium.classes.computer import Computer


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
    computer = Computer("Model 3")
    jump = Software("Jump Control", 2)

    ship.add_computer(computer)
    assert ship.get_total_cost() == 4.0

    ship.modify_software(jump)
    assert ship.get_total_cost() == 4.2
    assert len(ship.software) == 1


def test_downgrading():
    # Testing adding a single piece of software to a ship
    ship = Spacecraft(100)
    computer = Computer("Model 3")
    jump = Software("Jump Control", 2)
    downgrade = Software("Jump Control", 1)

    ship.add_computer(computer)
    assert ship.get_total_cost() == 4.0

    # Adding the level 2 jump
    ship.modify_software(jump)
    assert ship.get_total_cost() == 4.2
    assert len(ship.software) == 1

    # Downgrading to the level 1 jump
    ship.modify_software(downgrade)
    assert ship.get_total_cost() == 4.1
    assert len(ship.software) == 1


def test_check_ratio():
    # Tests the available rating check
    ship = Spacecraft(100)
    computer = Computer("Model 3")
    jump = Software("Jump Control", 2)

    ship.add_computer(computer)
    assert ship.get_total_cost() == 4.0

    # Check before addition
    assert ship.check_rating_ratio() == 15

    # Adding the level 2 jump
    ship.modify_software(jump)
    assert ship.get_total_cost() == 4.2
    assert len(ship.software) == 1

    # Check after addition
    assert ship.check_rating_ratio() == 5


def test_remove():
    # Tests the available rating check
    ship = Spacecraft(100)
    computer = Computer("Model 3")
    jump = Software("Jump Control", 2)

    ship.add_computer(computer)
    assert ship.get_total_cost() == 4.0

    # Adding the level 2 jump
    ship.modify_software(jump)
    assert ship.get_total_cost() == 4.2
    assert len(ship.software) == 1

    # Removing
    ship.remove_software("Jump Control")
    assert ship.get_total_cost() == 4.0
    assert len(ship.software) == 0
