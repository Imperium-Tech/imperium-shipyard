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


def test_edit_tonnage(window):
    """ Tests for editing the tonnage of the ship """
    assert window is not None

    # Check setting the same tonnage
    window.edit_tonnage()
    assert window.spacecraft.tonnage == 100

    # Set index to 200
    window.tonnage_box.setCurrentIndex(1)
    window.edit_tonnage()

    # Check for values
    assert window.spacecraft.tonnage == 200
    assert window.spacecraft.get_remaining_cargo() == 190
    assert window.spacecraft.get_total_cost() == 9.0
    assert window.cost_line_edit.text() == "9.000"


def test_tonnage_drive(window):
    """
    Test for automatically upgrading to lowest available drive on new tonnage
    Tests for basic functionality of adding drives, as well
    """
    assert window is not None

    # Add drives to ship
    window.jump_line_edit.setText("A")
    window.edit_jdrive()

    window.thrust_line_edit.setText("A")
    window.edit_mdrive()

    window.pplant_line_edit.setText("A")
    window.edit_pplant()

    assert window.jump_label.text() == "A"
    assert window.thrust_label.text() == "A"
    assert window.pplant_label.text() == "A"

    # Set tonnage to 300, which requires B base drives
    window.tonnage_box.setCurrentIndex(2)
    window.edit_tonnage()

    assert window.spacecraft.tonnage == 300
    assert window.jump_label.text() == "B" and window.spacecraft.jdrive.drive_type == "B"
    assert window.thrust_label.text() == "B" and window.spacecraft.mdrive.drive_type == "B"
    assert window.pplant_label.text() == "B" and window.spacecraft.pplant.type == "B"


def test_hardpoint_counter(window):
    """ Tests hardpoint counter changing on new tonnage """
    assert window is not None

    # Check hardpoint counter at 100 tonnage
    assert window.total_hp.text() == "1"
    assert window.avail_hp.text() == "1"

    # Change tonnage and check again
    window.tonnage_box.setCurrentIndex(1)
    window.edit_tonnage()

    assert window.total_hp.text() == "2"
    assert window.avail_hp.text() == "2"


def test_edit_fuel(window):
    """ Simple test for editing fuel """
    assert window is not None

    assert window.spacecraft.get_remaining_cargo() == 90
    window.fuel_line_edit.setText("50")
    window.edit_fuel()
    assert window.spacecraft.get_remaining_cargo() == 40


def test_valid_drive_type(window):
    """ Tests some alphas for the valid drive function """
    assert window is not None

    assert window.check_valid_type("A") is True
    assert window.check_valid_type("a") is True
    assert window.check_valid_type("AA") is False
    assert window.check_valid_type("I") is False
    assert window.check_valid_type("O") is False


def test_edit_armor(window):
    """ Tests editing armor for the spacecraft """
    assert window is not None

    # Test adding no armor
    window.edit_armor()
    assert window.spacecraft.armour_total == 0
    assert len(window.spacecraft.armour) == 0

    # Add a piece of armor
    window.armor_combo_box.setCurrentIndex(1)
    window.edit_armor()

    # Check values
    assert window.spacecraft.armour_total == 2
    assert len(window.spacecraft.armour) == 1


def test_edit_hull_config(window):
    """ Tests editing the hull config """
    assert window is not None

    # Tests swapping to Streamlined and checking fuel scoops
    window.hull_config_box.setCurrentIndex(1)
    window.edit_hull_config()

    assert window.spacecraft.hull_type.type == "Streamlined"
    assert window.fuel_scoop.isChecked() is True

    # Tests distributed and fuel scoops
    window.hull_config_box.setCurrentIndex(2)
    window.edit_hull_config()

    assert window.spacecraft.hull_type.type == "Distributed"
    assert window.fuel_scoop.isChecked() is False


def test_modify_hull_option(window):
    """ Tests editing a hull option """
    assert window is not None

    # Tests checking self-seal
    window.seal_check.setChecked(True)
    assert window.seal_check.isChecked() is True
    assert window.spacecraft.get_total_cost() == 3.5

    # Tests unchecking it
    window.seal_check.setChecked(False)
    assert window.seal_check.isChecked() is False
    assert window.spacecraft.get_total_cost() == 2.5


def test_modify_screen(window):
    """ Tests modifying the screen """
    assert window is not None

    # Tests checking the meson screen
    window.meson_screen.setChecked(True)
    assert window.meson_screen.isChecked() is True
    assert window.spacecraft.get_total_cost() == 62.5
    assert window.spacecraft.get_remaining_cargo() == 40

    # Tests unchecking
    # Tests checking the meson screen
    window.meson_screen.setChecked(False)
    assert window.meson_screen.isChecked() is False
    assert window.spacecraft.get_total_cost() == 2.5
    assert window.spacecraft.get_remaining_cargo() == 90


def test_edit_sensors(window):
    """ Tests modifying the sensors """
    assert window is not None

    # Tests setting the sensor to basic military
    window.sensors.setCurrentIndex(2)
    window.edit_sensors()

    assert window.spacecraft.sensors.name == "Basic Military"
    assert window.spacecraft.get_remaining_cargo() == 88
    assert window.spacecraft.get_total_cost() == 3.5


def test_edit_computer(window):
    """ Tests modifying the computer model """
    assert window is not None

    # Set to model tier 1
    window.computers.setCurrentIndex(1)
    window.edit_computer()

    assert window.spacecraft.computer.model == "Model 1"
    assert window.spacecraft.get_total_cost() == 2.53

    # Test adding computer addon
    window.jump_control_spec.setChecked(True)
    assert window.spacecraft.computer.bis is True
    assert window.spacecraft.get_total_cost() == 2.545

    # Set computer to none
    window.computers.setCurrentIndex(0)
    window.edit_computer()

    assert window.spacecraft.computer is None
    assert window.spacecraft.get_total_cost() == 2.5


def test_modifying_software(window):
    """ Tests adding/removing software to the ship """
    assert window is not None

    # Get starting box count
    box_count = window.software_box.count()

    # Add jump control
    window.software_box.setCurrentIndex(1)
    window.add_software(window.software_box)

    # Check stats and box removal
    assert len(window.spacecraft.software) == 1
    assert window.spacecraft.get_total_cost() == 2.6
    assert window.software_box.count() == box_count - 1

    # Remove software
    label = window.computer_config_layout.itemAt(13).widget()
    window.remove_software(label)

    assert len(window.spacecraft.software) == 0
    assert window.spacecraft.get_total_cost() == 2.5
    assert window.software_box.count() == box_count


def test_mod_software_level(window):
    """ Tests modifying software level """
    assert window is not None

    # Add software
    window.software_box.setCurrentIndex(1)
    window.add_software(window.software_box)

    # Modify software level
    box = window.computer_config_layout.itemAt(14).widget()
    box.setCurrentIndex(1)

    # Check stats
    assert window.spacecraft.get_total_cost() == 2.7


def test_modify_misc(window):
    """ Tests adding and modifying a misc """
    assert window is not None

    # Test adding invalid misc
    window.add_misc(window.misc_box)
    assert window.spacecraft.get_total_cost() == 2.5
    assert window.spacecraft.get_remaining_cargo() == 90

    # Add stateroom and check stats
    window.misc_box.setCurrentIndex(2)
    window.add_misc(window.misc_box)

    assert window.spacecraft.get_total_cost() == 3.0
    assert window.spacecraft.get_remaining_cargo() == 86
    assert len(window.spacecraft.misc) == 1

    # Modify stateroom
    label = window.misc_config_layout.itemAt(3).widget()
    line_edit = window.misc_config_layout.itemAt(4).widget()
    line_edit.setText("2")
    window.modify_misc_item(label, line_edit)

    assert window.spacecraft.get_remaining_cargo() == 82
    assert window.spacecraft.get_total_cost() == 3.5

    # Remove stateroom
    window.remove_misc(label)
    assert window.spacecraft.get_total_cost() == 2.5
    assert window.spacecraft.get_remaining_cargo() == 90
    assert window.misc_config_layout.itemAt(3) is None


def test_add_hardpoint(window):
    """ Tests adding a hardpoint to the ship """
    assert window is not None

    # Add hardpoint
    window.add_hardpoint()
    assert len(window.spacecraft.hardpoints) == 1
    assert window.hp_config_layout.itemAt(5).widget() is not None
    assert window.total_hp.text() == "1"
    assert window.avail_hp.text() == "0"

    # Remove hardpoint
    window.remove_hardpoint(window.spacecraft.hardpoints[0])
    assert len(window.spacecraft.hardpoints) == 0
    assert window.hp_config_layout.itemAt(5) is None
    assert window.total_hp.text() == "1"
    assert window.avail_hp.text() == "1"


def test_display_turret(window):
    """ Tests displaying the turret of a hardpoint """
    assert window is not None

    # Add hardpoint and call display
    window.add_hardpoint()
    window.add_hardpoint()
    window.display_turret(window.turret_config_layout, window.active_hp_buttons[0], window.spacecraft.hardpoints[0])

    # Check for proper displays
    name = "---- HP: {} ----".format(window.spacecraft.hardpoints[0].id)
    assert window.turret_config_layout.itemAt(0).widget().text() == name
    assert window.turret_config_layout.itemAt(2).widget().currentText() == "---"


def test_display_turret_with_wep(window):
    """ Tests displaying the turret of a hardpoint that has a weapon """
    assert window is not None

    # Add hardpoint and display turret
    window.add_hardpoint()
    window.display_turret(window.turret_config_layout, window.active_hp_buttons[0], window.spacecraft.hardpoints[0])

    # Change turret to single model
    window.turret_config_layout.itemAt(2).widget().setCurrentIndex(1)
    assert window.spacecraft.hardpoints[0].turret is not None
    assert window.spacecraft.get_total_cost() == 2.7
    assert window.spacecraft.get_remaining_cargo() == 89

    # Add weapon to turret
    window.turret_config_layout.itemAt(8).widget().setCurrentIndex(1)
    assert window.spacecraft.get_remaining_cargo() == 89
    assert window.spacecraft.get_total_cost() == 3.2

    # Swap turret model to bayweapon
    window.turret_config_layout.itemAt(2).widget().setCurrentIndex(4)
    assert window.spacecraft.get_remaining_cargo() == 39
    assert window.spacecraft.get_total_cost() == 2.5

    # Remove turret, back to '---'
    window.turret_config_layout.itemAt(2).widget().setCurrentIndex(0)
    assert window.spacecraft.get_remaining_cargo() == 90
    assert window.spacecraft.get_total_cost() == 2.5
    assert window.spacecraft.hardpoints[0].turret is None


def test_turret_ammo(window):
    """ Tests modifying ammunition on a turret """
    assert window is not None

    window.add_hardpoint()
    window.display_turret(window.turret_config_layout, window.active_hp_buttons[0], window.spacecraft.hardpoints[0])

    # Change turret to single model
    window.turret_config_layout.itemAt(2).widget().setCurrentIndex(1)

    # Modify missile ammo
    window.turret_config_layout.itemAt(15).widget().setText("1")

    turret = window.spacecraft.hardpoints[0].turret
    ammo_type = window.turret_config_layout.itemAt(13).widget().text()[:-10]
    total_label = window.turret_config_layout.itemAt(14).widget()
    edit = window.turret_config_layout.itemAt(15).widget()

    window.modify_turret_ammo(turret, ammo_type, total_label, edit)
    assert window.spacecraft.get_total_cost() == 2.715
    assert window.spacecraft.get_remaining_cargo() == 88
    assert window.spacecraft.hardpoints[0].turret.missiles.get(ammo_type) == 1


def test_sandcaster_ammo(window):
    """ Tests modifying sandcaster ammo on a turret """
    assert window is not None

    window.add_hardpoint()
    window.display_turret(window.turret_config_layout, window.active_hp_buttons[0], window.spacecraft.hardpoints[0])

    # Change turret to single model
    window.turret_config_layout.itemAt(2).widget().setCurrentIndex(1)

    # Modify sandcaster ammo
    window.turret_config_layout.itemAt(24).widget().setText("1")

    turret = window.spacecraft.hardpoints[0].turret
    total_label = window.turret_config_layout.itemAt(23).widget()
    edit = window.turret_config_layout.itemAt(24).widget()
    window.modify_turret_sandcaster(turret, total_label, edit)

    assert window.spacecraft.get_total_cost() == 2.710
    assert window.spacecraft.get_remaining_cargo() == 88
    assert window.spacecraft.hardpoints[0].turret.sandcaster_barrels == 1