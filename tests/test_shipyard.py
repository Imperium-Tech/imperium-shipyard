"""
@file test_shipyard.py

Unit tests for the Shipyard.py
"""
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtTest
from imperium.shipyard import Window
import sys


def test_init():
    app = QApplication(sys.argv)

    window = Window()
    assert window is not None
    assert window.spacecraft.tonnage == 0
    assert window.logger.text() == ""
    assert window.tonnage_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "0"
    assert window.fuel_line_edit.text() == "0"
    assert window.jump_line_edit.text() == "0"
    assert window.jump_label.text() == "-"
    assert window.thrust_line_edit.text() == "0"
    assert window.thrust_label.text() == "-"
    assert window.hull_hp_line_edit.text() == "0"
    assert window.structure_hp_line_edit.text() == "0"
    assert window.armour_line_edit.text() == "0"
    assert window.cost_line_edit.text() == "0.0"


def test_set_tonnage():
    app = QApplication(sys.argv)

    window = Window()
    tonnage = window.tonnage_line_edit
    tonnage.setText("200")
    window.edit_tonnage()
    window.update_stats()

    assert window.spacecraft.tonnage == 200
    assert window.spacecraft.cargo == 200
    assert window.spacecraft.cost_total == 8.0
    assert window.tonnage_line_edit.text() == "200"
    assert window.cargo_line_edit.text() == "200"
    assert window.cost_line_edit.text() == "8.0"
    assert window.hull_hp_line_edit.text() == "4"
    assert window.structure_hp_line_edit.text() == "4"
