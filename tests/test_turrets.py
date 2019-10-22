"""
@file test_turrets.py

File to test functionality of the Turrets class
"""
import pytest
from imperium.models.turrets import Turret


def test_single_turret():
    """
    Test to check single turret initialization and the weapon remove functionality
    """
    print("--- Test for Single Turret ---")
    turret = Turret("Single Turret")
    assert turret.tonnage == 1
    assert turret.get_cost() == 0.2
    assert turret.max_wep == 1

    turret.modify_weapon("Pulse Laser", 0)
    assert turret.tonnage == 1
    assert turret.get_cost() == 0.7

    turret.modify_weapon("---", 0)

    turret.modify_weapon("Beam Laser", 0)
    assert turret.tonnage == 1
    assert turret.get_cost() == 1.2
    assert turret.max_wep == 1

    turret.modify_weapon("---", 0)
    print("--- Passed test for Single Turret! ---")


def test_double_turret():
    """
    Test to check double turret initialization as well as the "Pop-up Turret" addon functionality
    :return:
    """
    print("--- Test for Double Turret ---")

    # Init of a double turret
    turret = Turret("Double Turret")
    assert turret.tonnage == 1
    assert turret.get_cost() == 0.5
    assert turret.max_wep == 2

    # Adding and removing weapons
    turret.modify_weapon("Pulse Laser", 0)
    assert turret.tonnage == 1
    assert turret.get_cost() == 1.0

    turret.modify_weapon("Beam Laser", 1)
    assert turret.tonnage == 1
    assert turret.get_cost() == 2.0

    turret.modify_weapon("---", 0)
    assert turret.tonnage == 1
    assert turret.get_cost() == 1.5

    print("--- Passed test for Double Turret! ---")


def test_triple_turret():
    print("--- Test for Triple Turret ---")

    # Init of a triple turret
    turret = Turret("Triple Turret")
    assert turret.tonnage == 1
    assert turret.get_cost() == 1.0
    assert turret.max_wep == 3

    # Adding three weapons
    turret.modify_weapon("Pulse Laser", 0)
    assert turret.tonnage == 1
    assert turret.get_cost() == 1.5

    turret.modify_weapon("Beam Laser", 1)
    assert turret.tonnage == 1
    assert turret.get_cost() == 2.5

    turret.modify_weapon("Pulse Laser", 2)
    assert turret.tonnage == 1
    assert turret.get_cost() == 3.0

    print("--- Passed test for Triple Turret! ---")
