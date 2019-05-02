"""
@file test_bridge.py

Unit tests for bridge component adding for a ship
"""
import pytest
from imperium.models.spacecraft import Spacecraft


def test_small():
    spacecraft = Spacecraft(100)
    spacecraft.set_bridge()

    assert spacecraft.get_remaining_cargo() == 90
    assert spacecraft.get_total_cost() == 2.5


def test_medium():
    spacecraft = Spacecraft(400)
    spacecraft.set_bridge()

    assert spacecraft.get_remaining_cargo() == 380
    assert spacecraft.get_total_cost() == 18.0


def test_large():
    spacecraft = Spacecraft(1200)
    spacecraft.set_bridge()

    assert spacecraft.get_remaining_cargo() == 1170
    assert spacecraft.get_total_cost() == 126.0


def test_bigly():
    spacecraft = Spacecraft(2000)
    spacecraft.set_bridge()

    assert spacecraft.get_remaining_cargo() == 1960
    assert spacecraft.get_total_cost() == 210.0

