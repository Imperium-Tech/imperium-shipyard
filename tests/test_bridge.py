"""
@file test_bridge.py

Unit tests for bridge component adding for a ship
"""
import pytest
from shipyard.models.spacecraft import Spacecraft


def test_small():
    spacecraft = Spacecraft(100)
    spacecraft.add_bridge()

    assert spacecraft.cargo == 90
    assert spacecraft.cost_total == 2.5


def test_medium():
    spacecraft = Spacecraft(450)
    spacecraft.add_bridge()

    assert spacecraft.cargo == 430
    assert spacecraft.cost_total == 34.0


def test_large():
    spacecraft = Spacecraft(1200)
    spacecraft.add_bridge()

    assert spacecraft.cargo == 1160
    assert spacecraft.cost_total == 126.0


def test_bigly():
    spacecraft = Spacecraft(2000)
    spacecraft.add_bridge()

    assert spacecraft.cargo == 1940
    assert spacecraft.cost_total == 210.0

