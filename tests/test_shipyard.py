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
    # Test init of the window and its starting values
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


def test_edit_tonnage():
    # Test setting tonnage and checking GUI updates
    app = QApplication(sys.argv)

    window = Window()
    window.tonnage_line_edit.setText("200")
    window.edit_tonnage()
    window.update_stats()

    assert window.spacecraft.tonnage == 200
    assert window.spacecraft.cargo == 200
    assert window.spacecraft.cost_total == 8.0
    assert window.spacecraft.hull_hp == 4
    assert window.spacecraft.structure_hp == 4
    assert window.tonnage_line_edit.text() == "200"
    assert window.cargo_line_edit.text() == "200"
    assert window.cost_line_edit.text() == "8.0"
    assert window.hull_hp_line_edit.text() == "4"
    assert window.structure_hp_line_edit.text() == "4"


"""
FUEL TESTS
"""
def test_edit_fuel():
    # Test setting fuel and GUI updates
    app = QApplication(sys.argv)

    window = Window()
    window.tonnage_line_edit.setText("100")
    window.edit_tonnage()

    window.fuel_line_edit.setText("50")
    window.edit_fuel()
    window.update_stats()

    assert window.spacecraft.fuel_max == 50
    assert window.spacecraft.cargo == 50
    assert window.fuel_line_edit.text() == "50"
    assert window.cargo_line_edit.text() == "50"


"""
JDRIVE TESTS
"""
def test_edit_jdrive_valid():
    # Test valid jdrive edit
    app = QApplication(sys.argv)

    window = Window()
    window.tonnage_line_edit.setText("100")
    window.edit_tonnage()

    window.jump_line_edit.setText("A")
    window.edit_jdrive()
    window.update_stats()

    assert window.spacecraft.jdrive is not None
    assert window.spacecraft.jump == 2
    assert window.spacecraft.cargo == 90
    assert window.spacecraft.cost_total == 12.0
    assert window.jump_line_edit.text() == "2"
    assert window.cargo_line_edit.text() == "90"
    assert window.jump_label.text() == "A"
    assert window.cost_line_edit.text() == "12.0"


def test_edit_jdrive_invalid():
    # Test invalid jdrive edit
    app = QApplication(sys.argv)

    window = Window()
    window.tonnage_line_edit.setText("100")
    window.edit_tonnage()

    window.jump_line_edit.setText("AAB")
    window.edit_jdrive()
    window.update_stats()

    assert window.spacecraft.jdrive is None
    assert window.spacecraft.jump == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.jump_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.jump_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"

    window.jump_line_edit.setText("I")
    window.edit_jdrive()
    window.update_stats()

    assert window.spacecraft.jdrive is None
    assert window.spacecraft.jump == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.jump_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.jump_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"

    window.jump_line_edit.setText("O")
    window.edit_jdrive()
    window.update_stats()

    assert window.spacecraft.jdrive is None
    assert window.spacecraft.jump == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.jump_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.jump_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"

    window.jump_line_edit.setText("__")
    window.edit_jdrive()
    window.update_stats()

    assert window.spacecraft.jdrive is None
    assert window.spacecraft.jump == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.jump_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.jump_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"


def test_jdrive_invalid_type():
    app = QApplication(sys.argv)

    window = Window()
    window.tonnage_line_edit.setText("100")
    window.edit_tonnage()

    window.jump_line_edit.setText("Z")
    window.edit_jdrive()
    window.update_stats()

    assert window.spacecraft.jdrive is None
    assert window.spacecraft.jump == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.jump_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.jump_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"
    assert window.logger.text() == "Error: non-compatible drive to tonnage value - Drive Z to 100"


"""
MDRIVE TESTS
"""
def test_edit_mdrive_valid():
    # Test valid mdrive edit
    app = QApplication(sys.argv)

    window = Window()
    window.tonnage_line_edit.setText("100")
    window.edit_tonnage()

    window.thrust_line_edit.setText("A")
    window.edit_mdrive()
    window.update_stats()

    assert window.spacecraft.mdrive is not None
    assert window.spacecraft.thrust == 2
    assert window.spacecraft.cargo == 98
    assert window.spacecraft.cost_total == 6.0
    assert window.thrust_line_edit.text() == "2"
    assert window.cargo_line_edit.text() == "98"
    assert window.thrust_label.text() == "A"
    assert window.cost_line_edit.text() == "6.0"


def test_edit_mdrive_invalid():
    # Test invalid mdrive edits
    app = QApplication(sys.argv)

    window = Window()
    window.tonnage_line_edit.setText("100")
    window.edit_tonnage()

    window.thrust_line_edit.setText("AAB")
    window.edit_mdrive()
    window.update_stats()

    assert window.spacecraft.mdrive is None
    assert window.spacecraft.thrust == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.thrust_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.thrust_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"

    window.thrust_line_edit.setText("I")
    window.edit_mdrive()
    window.update_stats()

    assert window.spacecraft.mdrive is None
    assert window.spacecraft.thrust == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.thrust_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.thrust_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"

    window.thrust_line_edit.setText("O")
    window.edit_mdrive()
    window.update_stats()

    assert window.spacecraft.mdrive is None
    assert window.spacecraft.thrust == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.thrust_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.thrust_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"

    window.thrust_line_edit.setText("___")
    window.edit_mdrive()
    window.update_stats()

    assert window.spacecraft.mdrive is None
    assert window.spacecraft.thrust == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.thrust_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.thrust_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"


def test_mdrive_invalid_type():
    # Testing too high mdrive for tonnage
    app = QApplication(sys.argv)

    window = Window()
    window.tonnage_line_edit.setText("100")
    window.edit_tonnage()

    window.thrust_line_edit.setText("Z")
    window.edit_mdrive()
    window.update_stats()

    assert window.spacecraft.mdrive is None
    assert window.spacecraft.thrust == 0
    assert window.spacecraft.cargo == 100
    assert window.spacecraft.cost_total == 2.0
    assert window.thrust_line_edit.text() == "0"
    assert window.cargo_line_edit.text() == "100"
    assert window.thrust_label.text() == "-"
    assert window.cost_line_edit.text() == "2.0"
    assert window.logger.text() == "Error: non-compatible drive to tonnage value - Drive Z to 100"

