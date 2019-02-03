"""
@file test_jump_thrust.py

Unit test for testing jump and thrust functionality for m- and j-drives
"""
import pytest
from shipyard.models.spacecraft import Spacecraft


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
