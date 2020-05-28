"""
@file test_computer.py

Unit tests for testing functionality of adding and replacing a computer system in a ship
"""
import pytest
from imperium.classes.computer import Computer
from imperium.classes.spacecraft import Spacecraft


def test_init():
    # Test ship rating check before computer addition
    ship = Spacecraft(100)
    assert ship.check_rating_ratio() == 0

    # Initializing a computer and adding a mod to it, testing the end values
    computer = Computer("Model 5")
    assert computer.rating == 25
    assert computer.tl == 13
    assert computer.get_cost() == 10.0

    computer.modify_addon("Jump Control Spec")
    assert computer.rating == 25
    assert computer.get_cost() == 15.0

    computer.modify_addon("Hardened System")
    assert computer.get_cost() == 20.0


def test_adding():
    # Initializing a ship and adding a computer system to it, checking for correct values
    ship = Spacecraft(100)
    assert ship.get_total_cost() == 2.0

    computer = Computer("Model 3")
    ship.add_computer(computer)
    assert ship.get_total_cost() == 4.0
    assert ship.check_rating_ratio() == 15


def test_swapping():
    # Test swapping between computer models
    ship = Spacecraft(100)
    assert ship.get_total_cost() == 2.0

    computer = Computer("Model 3")
    ship.add_computer(computer)
    assert ship.get_total_cost() == 4.0
    assert ship.check_rating_ratio() == 15

    new = Computer("Model 4")
    ship.add_computer(new)
    assert ship.get_total_cost() == 7.0
    assert ship.check_rating_ratio() == 20
