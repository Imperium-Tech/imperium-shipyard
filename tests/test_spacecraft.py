"""
test_spacecraft.py

Unit tests for classes in shipyard.models.spacecraft
"""
import pytest
from shipyard.models.spacecraft import Spacecraft


def test_spacecraft_init():
    """
    Tests the initialization of a new Spacecraft (hull)
    """
    spacecraft = Spacecraft(1000)
    assert spacecraft.tonnage == 1000
    assert spacecraft.cargo == 1000
    assert spacecraft.hull_hp == 1000 // 50
    assert spacecraft.structure_hp == 1000 // 50
    assert spacecraft.cost_hull == 100
    assert spacecraft.cost_total == 100
