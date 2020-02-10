"""
@file test_shipyard

Holds the unit tests for shipyard.py, which is mainly PyQT interactions
"""
import sys
import pytest
from pytestqt import qtbot
from imperium.shipyard import Window


@pytest.fixture()
def window(qtbot):
    """ Before all for the tests, initializing a Window object """
    window = Window()
    qtbot.addWidget(window)
    yield window


def test_base_stats_init(window):
    """ Tests for a base init of the Base Stats """
    assert window is not None
    assert window.spacecraft.tonnage == 100

    # Base Stats
    assert window.spacecraft.get_remaining_cargo() == 90
    assert window.cargo_line_edit.text() == "90"

    assert window.fuel_line_edit.text() == "0"
    assert window.jump_line_edit.text() == "0"
    assert window.jump_label.text() == "-"
    assert window.thrust_line_edit.text() == "0"
    assert window.thrust_label.text() == "-"

    assert window.hull_hp_line_edit.text() == "2"
    assert window.structure_hp_line_edit.text() == "2"
    assert window.armour_line_edit.text() == "0"

    assert window.discount.text() == "0"
    assert window.cost_line_edit.text() == "2.500"


def test_config_init(window):
    """ Tests for base init of Config/Armor group """
    assert window is not None

    assert window.bridge_check.isChecked() is True
    assert window.reflec_check.isChecked() is False
    assert window.seal_check.isChecked() is False
    assert window.stealth_check.isChecked() is False

    assert window.meson_screen.isChecked() is False
    assert window.nuclear_damper.isChecked() is False
    assert window.fuel_scoop.isChecked() is False

    assert window.hull_config_box.currentText() == "Standard"
    assert window.sensors.currentText() == "Standard"
    assert window.armor_combo_box.currentText() == "---"

