"""
@file test_bayweapons.py

Unit tests for testing functionality of adding a bayweapon to a ship
"""
import pytest
from imperium.models.bayweapon import Bayweapon
from imperium.models.spacecraft import Spacecraft


def test_init():
    bayweapon = Bayweapon("Missile Bank")
    assert bayweapon.tl == 6
    assert bayweapon.range == "Special"
    assert bayweapon.damage is not None
    assert bayweapon.cost == 12


def test_add_remove():
    wep = Bayweapon("Missile Bank")
    print(wep)
    assert wep.tl == 6
    assert wep.range == "Special"
    assert wep.damage is not None
    assert wep.cost == 12

    ship = Spacecraft(100)
    assert ship.cost_total == 2
    assert ship.cargo == 100
    
    ship.add_bayweapon(wep)
    assert ship.cost_total == 14
    assert ship.cargo == 49

    ship.remove_bayweapon(wep)
    assert ship.cost_total == 2
    assert ship.cargo == 100

    # error checking for removing a non-existant bayweapon
    ship.remove_bayweapon(wep)
    assert ship.cost_total == 2
    assert ship.cargo == 100
