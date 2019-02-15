"""
@file test_jump_thrust.py

Unit test for testing jump and thrust functionality for m- and j-drives
"""
import pytest
from imperium.models.spacecraft import Spacecraft


def test_mdrive():
    # Testing valid drive to tonnage match
    spacecraft = Spacecraft(100)
    spacecraft.add_mdrive("A")
    assert spacecraft.thrust == 2

    # Testing invalid drive to tonnage match
    spacecraft = Spacecraft(100)
    spacecraft.add_mdrive("J")
    assert spacecraft.thrust == 0

    # Testing valid larger drive to tonnage match
    spacecraft = Spacecraft(2000)
    spacecraft.add_mdrive("U")
    assert spacecraft.thrust == 4


def test_jdrive():
    # Testing valid drive to tonnage match
    spacecraft = Spacecraft(200)
    spacecraft.add_jdrive("A")
    assert spacecraft.jump == 1

    # Testing invalid drive to tonnage match
    spacecraft = Spacecraft(100)
    spacecraft.add_jdrive("J")
    assert spacecraft.jump == 0

    # Testing valid larger drive to tonnage match
    spacecraft = Spacecraft(1600)
    spacecraft.add_jdrive("Z")
    assert spacecraft.jump == 5

