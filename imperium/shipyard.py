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

        # Add stat function
        def add_stat_to_layout(label, row, signal_function=None, force_int=False, read_only=False):
            """
            Adds all the necessary widgets to a grid layout for a single stat

            :param label: The label to display
            :param row: The row number to add on
            :param signal_function: An additional function to connect on edit
            :param force_int: Force input to be an integer value
            :param read_only: Make text field read only

            :returns: The QLineEdit object
            """
            new_label = QLabel(label)
            new_line_edit = QLineEdit()
            new_line_edit.setFixedWidth(50)
            new_line_edit.setValidator(QIntValidator(new_line_edit))

            if signal_function is not None:
                new_line_edit.editingFinished.connect(signal_function)
            if force_int:
                new_line_edit.setValidator(QIntValidator(new_line_edit))
            if read_only:
                new_line_edit.setReadOnly(True)
            
            new_line_edit.editingFinished.connect(self.update_stats)
            base_stats_layout.addWidget(new_label, row, 0)
            base_stats_layout.addWidget(new_line_edit, row, 2)

            return new_line_edit

        # Tonnage
        self.tonnage_line_edit = add_stat_to_layout("Tonnage:", 0, signal_function=self.edit_tonnage, force_int=True)

        # Cargo
        self.cargo_line_edit = add_stat_to_layout("Cargo:", 1, read_only=True)

        # Fuel
        self.fuel_line_edit = add_stat_to_layout("Fuel:", 2, signal_function=self.edit_fuel, force_int=True)

        # Jump
        self.jump_line_edit = add_stat_to_layout("Jump:", 3, read_only=True)

        # Thrust
        self.thrust_line_edit = add_stat_to_layout("Thrust:", 4, read_only=True)

        # Hull HP
        self.hull_hp_line_edit = add_stat_to_layout("Hull HP:", 5, read_only=True)

        # Structure HP
        self.structure_hp_line_edit = add_stat_to_layout("Structure HP:", 6, read_only=True)

        # Armor
        self.armour_line_edit = add_stat_to_layout("Armour:", 7, read_only=True)

        # Cost
        self.cost_line_edit = add_stat_to_layout("Cost:", 8, read_only=True)
        
        # Grid layout
        base_stats_group.setLayout(base_stats_layout)
        ###################################
        ###  END: Base Stats Grid       ###
        ###################################

        # Overall layout grid
        layout = QGridLayout()
        layout.addWidget(base_stats_group, 0, 0)
        self.setLayout(layout)

        # Update to current stats
        self.update_stats()

    def update_stats(self):
        """
        Updates the UI with the current Spacecraft stats
        """
        self.tonnage_line_edit.setText(str(      self.spacecraft.tonnage            ))
        self.cargo_line_edit.setText(str(        self.spacecraft.cargo              ))
        self.fuel_line_edit.setText(str(         self.spacecraft.fuel_max           ))
        self.jump_line_edit.setText(str(         self.spacecraft.jump               ))
        self.thrust_line_edit.setText(str(       self.spacecraft.thrust             ))
        self.hull_hp_line_edit.setText(str(      self.spacecraft.hull_hp            ))
        self.structure_hp_line_edit.setText(str( self.spacecraft.structure_hp       ))
        self.armour_line_edit.setText(str(       self.spacecraft.get_armor_rating() ))
        self.cost_line_edit.setText(str(         self.spacecraft.cost_total         ))

    def edit_tonnage(self):
        """
        Update the spacecraft tonnage
        """
        new_tonnage = int(self.tonnage_line_edit.text())
        self.spacecraft.set_tonnage(new_tonnage)

    def edit_fuel(self):
        """
        Update the spacecraft max fuel
        """
        new_fuel = int(self.fuel_line_edit.text())
        self.spacecraft.set_fuel(new_fuel)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
