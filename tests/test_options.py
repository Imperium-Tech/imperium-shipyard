"""
@file test_options.py

Unit tests for Options objects within a ship
"""
import pytest
from imperium.models.option import Option
from imperium.models.spacecraft import Spacecraft


def test_init():
    # Tests initialization both screen types
    reflec = Option("Reflec")
    assert reflec.name == "Reflec"
    assert reflec.cost_per_hull_ton == 0.1

    self_seal = Option("Self-Sealing")
    assert self_seal.name == "Self-Sealing"
    assert self_seal.cost_per_hull_ton == 0.01

    stealth = Option("Stealth")
    assert stealth.name == "Stealth"
    assert stealth.cost_per_hull_ton == 0.1


def test_adding():
    # Tests adding hull objects to the ship
    spacecraft = Spacecraft(100)
    reflec = Option("Reflec")
    stealth = Option("Stealth")

    spacecraft.modify_hull_option(reflec)
    assert spacecraft.get_remaining_cargo() == 100
    assert spacecraft.get_total_cost() == 12.0
    assert len(spacecraft.hull_options) == 1

    spacecraft.modify_hull_option(stealth)
    assert spacecraft.get_remaining_cargo() == 100
    assert spacecraft.get_total_cost() == 22.0
    assert len(spacecraft.hull_options) == 2


def test_removing():
    # Tests removing a hull object from the ship
    spacecraft = Spacecraft(100)
    reflec = Option("Reflec")

    spacecraft.modify_hull_option(reflec)
    assert spacecraft.get_remaining_cargo() == 100
    assert spacecraft.get_total_cost() == 12.0
    assert len(spacecraft.hull_options) == 1

    new_reflec = Option("Reflec")
    spacecraft.modify_hull_option(new_reflec)
    assert spacecraft.get_remaining_cargo() == 100
    assert spacecraft.get_total_cost() == 2.0
    assert len(spacecraft.hull_options) == 0
