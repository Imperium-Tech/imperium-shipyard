"""
shipyard.py

Entrypoint for the imperium-shipyard program (https://github.com/Milkshak3s/imperium-shipyard)
"""
from imperium.models.config import Config
from imperium.models.json_reader import get_file_data
from imperium.models.spacecraft import Spacecraft
from imperium.models.armor import Armor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
QLabel, QLineEdit, QWidget, QPushButton)


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
        self.tonnage_line_edit.validator().setBottom(0)

        # Cargo
        self.cargo_line_edit = add_stat_to_layout("Cargo:", 1, read_only=True)

        # Fuels
        self.fuel_line_edit = add_stat_to_layout("Fuel:", 2, signal_function=self.edit_fuel, force_int=True)
        self.fuel_line_edit.validator().setBottom(0)

        # Jump
        self.jump_line_edit = add_stat_to_layout("Jump:", 3, signal_function=self.edit_jdrive)
        self.jump_label = QLabel("-")
        base_stats_layout.addWidget(self.jump_label, 3, 1)

        # Thrust
        self.thrust_line_edit = add_stat_to_layout("Thrust:", 4, signal_function=self.edit_mdrive)
        self.thrust_label = QLabel("-")
        base_stats_layout.addWidget(self.thrust_label, 4, 1)

        # Hull HP
        self.hull_hp_line_edit = add_stat_to_layout("Hull HP:", 5, signal_function=self.edit_tonnage, read_only=True)

        # Structure HP
        self.structure_hp_line_edit = add_stat_to_layout("Structure HP:", 6, signal_function=self.edit_tonnage, read_only=True)

        # Armor
        self.armour_line_edit = add_stat_to_layout("Armour:", 7, read_only=True)

        # Cost
        self.cost_line_edit = add_stat_to_layout("Cost (MCr.):", 8, read_only=True)

        # Grid layout
        base_stats_group.setLayout(base_stats_layout)
        ###################################
        ###  END: Base Stats Grid       ###
        ###################################

        ###################################
        ###  START: Armor/Config Grid   ###
        ###################################
        self.armor_config_group = QGroupBox("Armor/Config")
        self.armor_config_layout = QGridLayout()
        self.armor_config_layout.setAlignment(Qt.AlignTop)

        # Configuration armor for the hull of the ship
        self.armor_config_layout.addWidget(QLabel("Hull Config: "), 0, 0)
        self.hull_config_box = QComboBox()
        for item in get_file_data("hull_config.json").keys():
            self.hull_config_box.addItem(item)
        self.hull_config_box.activated.connect(self.edit_hull_config)
        self.armor_config_layout.addWidget(self.hull_config_box, 1, 0)

        # Drop down list of the available armor to add
        self.armor_config_layout.addWidget(QLabel("Armour: "), 2, 0)
        self.armor_combo_box = QComboBox()
        self.armor_combo_box.addItem("---")
        for item in get_file_data("hull_armor.json").keys():
            self.armor_combo_box.addItem(item)
        self.armor_combo_box.activated.connect(self.edit_armor)

        self.occupied_rows = 3
        self.armor_config_layout.addWidget(self.armor_combo_box, self.occupied_rows, 0)
        self.armor_config_group.setLayout(self.armor_config_layout)
        ###################################
        ###  END: Armor/Config Grid     ###
        ###################################

        # Setting appropriate column widths
        base_stats_group.setFixedWidth(150)
        self.armor_config_group.setFixedWidth(225)

        # Overall layout grid
        layout = QGridLayout()
        layout.addWidget(base_stats_group, 0, 0)
        layout.addWidget(self.armor_config_group, 0, 1)
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
        self.armour_line_edit.setText(str(       self.spacecraft.armour_total       ))
        self.cost_line_edit.setText("{:0.1f}".format(self.spacecraft.cost_total))

    def edit_tonnage(self):
        """
        Update the spacecraft tonnage
        """
        new_tonnage = int(self.tonnage_line_edit.text())
        self.reset_hull_config()
        self.spacecraft.set_tonnage(new_tonnage)

    def edit_fuel(self):
        """
        Update the spacecraft max fuel
        """
        new_fuel = int(self.fuel_line_edit.text())
        self.spacecraft.set_fuel(new_fuel)

    def edit_jdrive(self):
        """
        Update the spacecraft jump drive
        """
        drive_type = self.jump_line_edit.text()
        if drive_type.isalpha() and len(drive_type) == 1:
            result = self.spacecraft.add_jdrive(drive_type)
            if result:
                self.jump_label.setText(drive_type)

    def edit_mdrive(self):
        """
        Update the spacecraft thrust drive
        """
        drive_type = self.thrust_line_edit.text()
        if drive_type.isalpha() and len(drive_type) == 1:
            result = self.spacecraft.add_mdrive(drive_type)
            if result:
                self.thrust_label.setText(drive_type)

    def edit_armor(self):
        """
        Add a new armor piece to the ship, creating a new button in the grid and adjusting values
        """
        armor_type = self.armor_combo_box.currentText()
        self.armor_combo_box.setCurrentIndex(0)

        # Error checking for invalid ship states
        if armor_type == "---":
            return
        if self.spacecraft.tonnage == 0:
            print("Error: Tonnage not set before adding armor.")
            return

        armor = Armor(armor_type)
        self.spacecraft.add_armour(armor)

        # Button to handle removing the piece of armor
        button = QPushButton()
        button.setCheckable(True)
        button.setText("{} - Protect: {} | TL: {}".format(armor.type, armor.protection, armor.tl))
        button.clicked.connect(lambda: self.remove_armor(armor))
        button.clicked.connect(button.deleteLater)

        # Adjusting values and adding widget
        self.occupied_rows += 1
        self.armor_config_layout.addWidget(button, self.occupied_rows, 0)
        self.update_stats()

    def remove_armor(self, armor):
        """
        Handles removing a piece of armor from the ship, as well as updating GUI to reflect changes
        :param armor:
        :return:
        """
        self.spacecraft.remove_armour(armor)
        self.occupied_rows -= 1
        self.update_stats()

    def edit_hull_config(self):
        """
        Handles editing the hull config with a new one, adjusting the GUI and values
        """
        text = self.hull_config_box.currentText()
        config = Config(text)
        self.spacecraft.edit_hull_config(config)
        self.update_stats()

    def reset_hull_config(self):
        """
        Handles resetting hull configuration to standard.
        Used before setting a new tonnage for correct value parsing
        """
        self.hull_config_box.setCurrentIndex(0)
        config = Config("Standard")
        self.spacecraft.edit_hull_config(config)
        self.update_stats()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
