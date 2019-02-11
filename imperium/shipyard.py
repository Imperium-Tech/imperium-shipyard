"""
shipyard.py

Entrypoint for the imperium-shipyard program (https://github.com/Milkshak3s/imperium-shipyard)
"""
import data_generators as dg
from models.spacecraft import Spacecraft
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
QLabel, QLineEdit, QWidget)


def add_stat_to_layout(label, row, layout, force_int=False, read_only=False):
    """
    Adds all the necessary widgets to a grid layout for a single stat

    :param label: The label to display
    :param row: The row number to add on
    :param layout: The QGridLyout object to apply widget to
    :param force_int: Force input to be an integer value
    :param read_only: Make text field read only

    :returns: The QLineEdit object
    """
    new_label = QLabel(label)
    new_line_edit = QLineEdit()
    new_line_edit.setFixedWidth(50)
    new_line_edit.setValidator(QIntValidator(new_line_edit))

    if force_int:
        new_line_edit.setValidator(QIntValidator(new_line_edit))
    if read_only:
        new_line_edit.setReadOnly(True)

    layout.addWidget(new_label, row, 0)
    layout.addWidget(new_line_edit, row, 2)

    return new_line_edit


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        # Create a placeholder Spacecraft
        self.spacecraft = Spacecraft(0)

        # Window Title
        self.setWindowTitle("Imperium Shipyard")

        ###################################
        ###  BEGIN: Base Stats Grid     ###
        ###################################
        base_stats_group = QGroupBox("Base Stats")
        base_stats_layout = QGridLayout()

        # Tonnage
        self.tonnage_line_edit = add_stat_to_layout("Tonnage:", 0, base_stats_layout, force_int=True)

        # Cargo
        self.cargo_line_edit = add_stat_to_layout("Cargo:", 1, base_stats_layout, read_only=True)

        # Fuel
        self.fuel_line_edit = add_stat_to_layout("Fuel:", 2, base_stats_layout, force_int=True)

        # Jump
        self.jump_line_edit = add_stat_to_layout("Jump:", 3, base_stats_layout, read_only=True)

        # Thrust
        self.thrust_line_edit = add_stat_to_layout("Thrust:", 4, base_stats_layout, read_only=True)

        # Hull HP
        self.hull_hp_line_edit = add_stat_to_layout("Hull HP:", 5, base_stats_layout, read_only=True)

        # Structure HP
        self.structure_hp_line_edit = add_stat_to_layout("Structure HP:", 6, base_stats_layout, read_only=True)

        # Armor
        self.armor_line_edit = add_stat_to_layout("Armor:", 7, base_stats_layout, read_only=True)

        # Cost
        self.cost_line_edit = add_stat_to_layout("Cost:", 8, base_stats_layout, read_only=True)
        
        # Grid layout
        base_stats_group.setLayout(base_stats_layout)
        ###################################
        ###  BEGIN: Base Stats Grid     ###
        ###################################

        # Overall layout grid
        layout = QGridLayout()
        layout.addWidget(base_stats_group, 0, 0)
        self.setLayout(layout)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
