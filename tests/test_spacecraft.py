"""
test_spacecraft.py

Unit tests for classes in shipyard.models.spacecraft
"""
import pytest
from shipyard.models.spacecraft import Spacecraft


@pytest.fixture
def spacecraft():
    """
    Fixture for a 1000 ton spacecraft for testing
    """
    new_spacecraft = Spacecraft(1000)
    return new_spacecraft


def test_spacecraft_init(spacecraft):
    """
    Tests the initialization of a new Spacecraft (hull)
    """
    assert spacecraft.tonnage == 1000
    assert spacecraft.cargo == 1000
    assert spacecraft.hull_hp == 1000 // 50
    assert spacecraft.structure_hp == 1000 // 50
    assert spacecraft.cost == 100
