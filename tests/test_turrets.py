"""
@file test_turrets.py

File to test functionality of the Turrets class
"""
import pytest
from shipyard.models.turrets import Turret


def test_single_turret():
    """
    Test to check single turret initialization and the weapon remove functionality
    """
    print("--- Test for Single Turret ---")
    turret = Turret("Single Turret")
    assert turret.tonnage == 1.0
    assert turret.cost == 0.2
    assert turret.max_wep == 1

    turret.add_weapon("Pulse Laser")
    assert turret.tonnage == 1.0
    assert turret.cost == 0.7
    assert len(turret.weapons) == 1

    turret.remove_weapon("Pulse Laser")

    turret.add_weapon("Beam Laser")
    assert turret.tonnage == 1.0
    assert turret.cost == 1.2
    assert turret.max_wep == 1

    turret.add_weapon("Particle Beam")
    print("--- Passed test for Single Turret! ---")


def test_double_turret():
    """
    Test to check double turret initialization as well as the "Pop-up Turret" addon functionality
    :return:
    """
    print("--- Test for Double Turret ---")

    # Init of a double turret
    turret = Turret("Double Turret")
    assert turret.tonnage == 1.0
    assert turret.cost == 0.5
    assert turret.max_wep == 2

    # Adding and removing weapons
    turret.add_weapon("Pulse Laser")
    assert turret.tonnage == 1.0
    assert turret.cost == 1.0
    assert len(turret.weapons) == 1

    turret.add_weapon("Beam Laser")
    assert turret.tonnage == 1.0
    assert turret.cost == 2.0
    assert len(turret.weapons) == 2

    turret.remove_weapon("Pulse Laser")
    assert turret.tonnage == 1.0
    assert turret.cost == 1.5
    assert len(turret.weapons) == 1

    # Testing pop-up turret add-on functionality
    turret.add_addon("Pop-up Turret")
    assert turret.tonnage == 3.0
    assert turret.cost == 2.5
    assert len(turret.weapons) == 1
    print("--- Passed test for Double Turret! ---")


def test_triple_turret():
    print("--- Test for Triple Turret ---")

    # Init of a triple turret
    turret = Turret("Triple Turret")
    assert turret.tonnage == 1.0
    assert turret.cost == 1.0
    assert turret.max_wep == 3

    # Adding three weapons
    turret.add_weapon("Pulse Laser")
    assert turret.tonnage == 1.0
    assert turret.cost == 1.5
    assert len(turret.weapons) == 1

    turret.add_weapon("Beam Laser")
    assert turret.tonnage == 1.0
    assert turret.cost == 2.5
    assert len(turret.weapons) == 2

    turret.add_weapon("Pulse Laser")
    assert turret.tonnage == 1.0
    assert turret.cost == 3.0
    assert len(turret.weapons) == 3

    # Testing add-on cost manipulation
    turret.add_addon("Fixed Mounting")
    assert turret.tonnage == 1.0
    assert turret.cost == 1.5
    print("--- Passed test for Triple Turret! ---")
