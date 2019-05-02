"""
shipyard.py

Entrypoint for the imperium-shipyard program (https://github.com/Milkshak3s/imperium-shipyard)
"""
from imperium.models.config import Config
from imperium.models.drives import MDrive, JDrive
from imperium.models.json_reader import get_file_data
from imperium.models.option import Option
from imperium.models.pplant import PPlant
from imperium.models.screens import Screen
from imperium.models.spacecraft import Spacecraft
from imperium.models.armour import Armour
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
                             QLabel, QLineEdit, QWidget, QPushButton, QCheckBox)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        # Create a placeholder Spacecraft
        self.spacecraft = Spacecraft(0)
        self.logger = QLabel("")

        # Window Title
        self.setWindowTitle("Imperium Shipyard")

        def add_combo_box(layout, label, json, funct, x, y, null_spot=False):
            """
            Handles adding a combo box widget with item names from a specific json file
            :param layout: PyQT layout
            :param label: label name
            :param json: name of the json file
            :param funct: function to connect items to
            :param x: row in layout
            :param y: col in layout
            :param null_spot: whether or not to have a 'null' box item
            :return: PyQT Combo Box
            """
            layout.addWidget(QLabel(label), x, y)
            combo_box = QComboBox()

            if null_spot:
                combo_box.addItem("---")
            for item in get_file_data(json).keys():
                combo_box.addItem(item)
            combo_box.activated.connect(funct)
            return combo_box

        def add_hull_option(layout, name, funct, x, y):
            """
            Handles adding a hull option component check box and attaching a function to it
            :param layout: which PyQT layout this widget belongs to
            :param name: name to be displayed on the GUI
            :param funct: function reference
            :param x: row in the groupbox
            :param y: column in the groupbox
            :return: the created QCheckBox
            """
            box = QCheckBox(name)
            box.stateChanged.connect(funct)
            layout.addWidget(box, x, y)
            return box

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
        base_stats_layout.addWidget(QLabel("Tonnage: "), 0, 0)
        self.tonnage_box = QComboBox()
        self.tonnage_box.addItem("0")
        for item in get_file_data("hull_data.json").values():
            tonnage = str(item.get('tonnage'))
            self.tonnage_box.addItem(tonnage)
        self.tonnage_box.activated.connect(self.edit_tonnage)
        base_stats_layout.addWidget(self.tonnage_box, 0, 2)

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

        # PPlant
        self.pplant_line_edit = add_stat_to_layout("PPlant:", 5, signal_function=self.edit_pplant)
        self.pplant_label = QLabel("-")
        base_stats_layout.addWidget(self.pplant_label, 5, 1)

        # Hull HP
        self.hull_hp_line_edit = add_stat_to_layout("Hull HP:", 6, signal_function=self.edit_tonnage, read_only=True)

        # Structure HP
        self.structure_hp_line_edit = add_stat_to_layout("Structure HP:", 7, signal_function=self.edit_tonnage, read_only=True)

        # Armor
        self.armour_line_edit = add_stat_to_layout("Armour:", 8, read_only=True)

        # Cost
        self.cost_line_edit = add_stat_to_layout("Cost (MCr.):", 9, read_only=True)

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

        #### Hull Options ###
        self.armor_config_layout.addWidget(QLabel("Hull Options:"), 0, 0)

        # Bridge
        self.bridge_check = add_hull_option(self.armor_config_layout, "Bridge", self.check_bridge, 1, 0)

        # Reflec
        self.reflec_check = add_hull_option(self.armor_config_layout, "Reflec",
                                            lambda: self.modify_hull_option(self.reflec_check), 2, 0)

        # Self-Sealing
        self.seal_check = add_hull_option(self.armor_config_layout, "Self-Sealing",
                                          lambda: self.modify_hull_option(self.seal_check), 3, 0)

        # Stealth
        self.stealth_check = add_hull_option(self.armor_config_layout, "Stealth",
                                             lambda: self.modify_hull_option(self.stealth_check), 4, 0)

        ### Screen Options ###
        self.armor_config_layout.addWidget(QLabel("Screen Options:"), 0, 1)

        # Meson Screen
        self.meson_screen = add_hull_option(self.armor_config_layout, "Meson Screen",
                                            lambda: self.modify_screen(self.meson_screen), 1, 1)

        # Nuclear Damper
        self.nuclear_damper = add_hull_option(self.armor_config_layout, "Nuclear Damper",
                                              lambda: self.modify_screen(self.nuclear_damper), 2, 1)

        ### Hull config list ###
        self.hull_config_box = add_combo_box(self.armor_config_layout, "Hull Config: ",
                                             "hull_config.json", self.edit_hull_config, 5, 0)
        self.armor_config_layout.addWidget(self.hull_config_box, 6, 0, 1, -1)

        ### Armor list ###
        self.armor_combo_box = add_combo_box(self.armor_config_layout, "Armour:",
                                             "hull_armor.json", self.edit_armor, 7, 0, True)

        self.occupied_rows = 8
        self.armor_config_layout.addWidget(self.armor_combo_box, self.occupied_rows, 0, 1, -1)
        self.armor_config_group.setLayout(self.armor_config_layout)
        ###################################
        ###  END: Armor/Config Grid     ###
        ###################################

        # Setting appropriate column widths
        base_stats_group.setFixedWidth(175)
        self.armor_config_group.setFixedWidth(275)

        # Overall layout grid
        layout = QGridLayout()
        layout.addWidget(base_stats_group, 0, 0)
        layout.addWidget(self.armor_config_group, 0, 1)
        layout.addWidget(self.logger, 1, 0, 1, -1)
        self.setLayout(layout)

        # Update to current stats
        self.update_stats()

    def update_stats(self):
        """
        Updates the UI with the current Spacecraft stats
        """
        self.cargo_line_edit.setText(str(        self.spacecraft.get_remaining_cargo()))
        self.fuel_line_edit.setText(str(         self.spacecraft.fuel_max           ))
        self.jump_line_edit.setText(str(         self.spacecraft.jump               ))
        self.thrust_line_edit.setText(str(       self.spacecraft.thrust             ))
        self.pplant_line_edit.setText(str(       self.spacecraft.fuel_two_weeks     ))
        self.hull_hp_line_edit.setText(str(      self.spacecraft.hull_hp            ))
        self.structure_hp_line_edit.setText(str( self.spacecraft.structure_hp       ))
        self.armour_line_edit.setText(str(       self.spacecraft.armour_total       ))
        self.cost_line_edit.setText("{:0.1f}".format(self.spacecraft.get_total_cost()))

        # Set the cargo text to red when cargo going negative
        if self.spacecraft.get_remaining_cargo() < 0:
            self.cargo_line_edit.setStyleSheet("color: red")
        else:
            self.cargo_line_edit.setStyleSheet("color: black")

        # Set the PPlant text red if its underfit
        validity = self.spacecraft.check_pplant_validity()
        if type(validity) is bool:
            self.pplant_line_edit.setStyleSheet("color: black")
        elif type(validity) is str:
            self.pplant_line_edit.setStyleSheet("color: red")
            self.logger.setText(validity)

    def edit_tonnage(self):
        """
        Update the spacecraft tonnage
        Updates the Drives to the lowest available type at that tonnage level
        """
        new_tonnage = int(self.tonnage_box.currentText())

        # Cap tonnage to 2000
        if new_tonnage > 2000:
            new_tonnage = 2000
        self.spacecraft.set_tonnage(new_tonnage)

        # Checks for updating the drive, if necessary
        if new_tonnage != 0 and (self.spacecraft.jdrive is not None or self.spacecraft.mdrive is not None):
            lowest_drive = self.spacecraft.get_lowest_drive()

            if self.spacecraft.jdrive is not None:
                self.jump_line_edit.setText(lowest_drive)
                self.edit_jdrive()
            if self.spacecraft.mdrive is not None:
                self.thrust_line_edit.setText(lowest_drive)
                self.edit_mdrive()
            if self.spacecraft.pplant is not None and self.spacecraft.pplant.type != lowest_drive:
                self.pplant_line_edit.setText(lowest_drive)
                self.edit_pplant()
        self.update_stats()

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
        drive_type = self.jump_line_edit.text().upper()
        if self.check_valid_type(drive_type):
            new_jdrive = JDrive(drive_type)
            result = self.spacecraft.add_jdrive(new_jdrive)
            if type(result) is str:
                self.logger.setText(result)
            else:
                self.jump_label.setText(drive_type)

    def edit_mdrive(self):
        """
        Update the spacecraft thrust drive
        """
        drive_type = self.thrust_line_edit.text().upper()
        if self.check_valid_type(drive_type):
            new_mdrive = MDrive(drive_type)
            result = self.spacecraft.add_mdrive(new_mdrive)
            if type(result) is str:
                self.logger.setText(result)
            else:
                self.thrust_label.setText(drive_type)

    def edit_pplant(self):
        """
        Update the spacecraft pplant drive
        """
        pplant_type = self.pplant_line_edit.text().upper()
        if self.check_valid_type(pplant_type):
            new_pplant = PPlant(pplant_type)
            result = self.spacecraft.add_pplant(new_pplant)
            if type(result) is bool:
                self.pplant_label.setText(pplant_type)
            elif type(result) is str:
                self.logger.setText(result)

    def check_valid_type(self, drive):
        """
        Checks whether input to the Drives is valid or not
        :param type: Type input to check
        :return: True iff it meets all criterion
        """
        return drive.isalpha() and len(drive) == 1 and drive != "I" and drive != "O"

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
            return self.logger.setText("Error: Tonnage not set before adding armor.")

        armor = Armour(armor_type)
        self.spacecraft.add_armour(armor)

        # Button to handle removing the piece of armor
        button = QPushButton()
        button.setCheckable(True)
        button.setText("{} - Protect: {} | TL: {}".format(armor.type, armor.protection, armor.tl))
        button.clicked.connect(lambda: self.remove_armor(armor))
        button.clicked.connect(button.deleteLater)

        # Adjusting values and adding widget
        self.occupied_rows += 1
        self.armor_config_layout.addWidget(button, self.occupied_rows, 0, 1, -1)
        self.update_stats()

    def remove_armor(self, armor):
        """
        Handles removing a piece of armor from the ship, as well as updating GUI to reflect changes
        :param armor: armour object to remove
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

    def check_bridge(self):
        # Handles bridge checkbox
        self.spacecraft.set_bridge()
        self.update_stats()

    def modify_hull_option(self, box):
        # Handles adding/removing a hull option
        opt_type = box.text()

        option = Option(opt_type)
        self.spacecraft.modify_hull_option(option)
        self.update_stats()

    def modify_screen(self, box):
        # Handles adding/removing a screen
        screen_type = box.text()

        screen = Screen(screen_type)
        self.spacecraft.modify_screen(screen)
        self.update_stats()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
