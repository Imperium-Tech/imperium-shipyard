"""
@file test_drives.py
@author qu-gg

Unit tests for functionality of the drive classes
"""
import pytest

from imperium.classes.pplant import PPlant
from imperium.classes.spacecraft import Spacecraft
from imperium.classes.drives import (JDrive, MDrive)


def test_init():
    """
    Tests initialization of both drive types
    """
    jdrive = JDrive("A")
    assert jdrive.drive_type == "A"
    assert jdrive.tonnage == 10
    assert jdrive.cost == 10

    mdrive = MDrive("A")
    assert mdrive.drive_type == "A"
    assert mdrive.tonnage == 2
    assert mdrive.cost == 4

    pplant = PPlant("A")
    assert pplant.fuel_two_weeks == 2
    assert pplant.cost == 8
    assert pplant.tonnage == 4


def test_adding():
    """
    Tests adding both types of drives to a ship
    """
    ship = Spacecraft(100)
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2
    assert ship.mdrive is None
    assert ship.jdrive is None

    ship.add_jdrive(JDrive("A"))
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 90
    assert ship.get_total_cost() == 12
    assert ship.jdrive is not None

    ship.add_mdrive(MDrive("A"))
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 88
    assert ship.get_total_cost() == 16
    assert ship.mdrive is not None

    ship.add_pplant(PPlant("A"))
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 84
    assert ship.get_total_cost() == 24
    assert ship.pplant is not None


def test_changing():
    """
    Tests changing a drive type from one to another
    """
    ship = Spacecraft(100)
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 100
    assert ship.get_total_cost() == 2
    assert ship.jdrive is None

    ship.add_jdrive(JDrive("A"))
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 90
    assert ship.get_total_cost() == 12
    assert ship.jdrive.drive_type == "A"

    ship.add_jdrive(JDrive("B"))
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 85
    assert ship.get_total_cost() == 22
    assert ship.jdrive.drive_type == "B"

    ship.add_mdrive(MDrive("A"))
    assert ship.get_remaining_cargo() == 83
    assert ship.get_total_cost() == 26
    assert ship.mdrive.drive_type == "A"

    ship.add_mdrive(MDrive("B"))
    assert ship.get_remaining_cargo() == 82
    assert ship.get_total_cost() == 30
    assert ship.mdrive.drive_type == "B"

    ship.add_pplant(PPlant("A"))
    assert ship.get_remaining_cargo() == 78
    assert ship.get_total_cost() == 38
    assert ship.pplant.type == "A"

    ship.add_pplant(PPlant("B"))
    assert ship.get_remaining_cargo() == 75
    assert ship.get_total_cost() == 46
    assert ship.pplant.type == "B"


def test_empty_ship():
    ship = Spacecraft(0)
    assert ship.tonnage == 0
    assert ship.get_remaining_cargo() == 0
    assert ship.jdrive is None

    ship.add_jdrive(JDrive("A"))
    assert ship.tonnage == 0
    assert ship.get_remaining_cargo() == 0
    assert ship.jdrive is None

    ship.add_mdrive(MDrive("A"))
    assert ship.tonnage == 0
    assert ship.get_remaining_cargo() == 0
    assert ship.mdrive is None

    ship.add_pplant(PPlant("A"))
    assert ship.tonnage == 0
    assert ship.get_remaining_cargo() == 0
    assert ship.pplant is None


def test_incompatible_drive():
    ship = Spacecraft(100)
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 100
    assert ship.mdrive is None

    ship.add_mdrive(MDrive("Z"))
    assert ship.mdrive is None


def test_pplant_validity():
    # Tests 4 cases for pplant validities
    ship = Spacecraft(100)
    assert ship.tonnage == 100
    assert ship.get_remaining_cargo() == 100

    ship.add_jdrive(JDrive("B"))
    ship.add_pplant(PPlant("B"))

    assert ship.check_pplant_validity() == True

    ship.add_pplant(PPlant("A"))
    assert ship.check_pplant_validity() == "Error: PPlant under J-Drive. A < B"

    ship = Spacecraft(100)
    ship.add_mdrive(MDrive("B"))
    ship.add_pplant(PPlant("A"))
    assert ship.check_pplant_validity() == "Error: PPlant under M-Drive. A < B"

    ship.add_jdrive(JDrive("B"))
    assert ship.check_pplant_validity() == "Error: PPlant under max M/J-Drive. A < B"