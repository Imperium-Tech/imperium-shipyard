"""
@file shipbuilder.py
@author Ryan Missel, Chris Vantine

Entrypoint for the imperium-shipyard program (https://github.com/Milkshak3s/imperium-shipyard)
Handles all of the UI interaction and display for the PyQT frontend
"""
import sys
import random
import os
import string

from imperium.classes.computer import Computer
from imperium.classes.config import Config
from imperium.classes.drives import MDrive, JDrive
from imperium.classes.hardpoint import Hardpoint
from imperium.classes.json_reader import get_file_data
from imperium.classes.misc import Misc
from imperium.classes.option import Option
from imperium.classes.pplant import PPlant
from imperium.classes.screens import Screen
from imperium.classes.sensors import Sensor
from imperium.classes.software import Software
from imperium.classes.spacecraft import Spacecraft
from imperium.classes.armour import Armour
from imperium.classes.turrets import Turret

from imperium.shipyard.fileloader import FileLoader

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox, QFileDialog,
                             QLabel, QLineEdit, QWidget, QFrame, QPushButton, QCheckBox,
                             QScrollArea, QMainWindow, QAction)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # Creating a file loader for saving
        self.fileloader = FileLoader()

        # Create a base Spacecraft to use
        self.spacecraft = Spacecraft(100)
        self.logger = QLabel("")

        # Window Title
        self.setWindowTitle("Imperium Shipyard - Untitled.srd")

        ###################################
        ###  BEGIN: Imperium Options    ###
        ###################################
        imperium_bar = self.menuBar()
        file_bar = imperium_bar.addMenu("File")

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(lambda: self.save_file())

        load_action = QAction("Load", self)
        load_action.triggered.connect(lambda: self.open_file())

        reset_action = QAction("Reset", self)
        reset_action.setShortcut("Ctrl+R")
        reset_action.triggered.connect(lambda: self.reset_ship())

        file_bar.addAction(save_action)
        file_bar.addAction(load_action)
        file_bar.addAction(reset_action)

        ###################################
        ###    END: Imperium Options    ###
        ###################################

        def add_combo_box(layout, label, json, funct, x, y, in_line=True, null_spot=False):
            """
            Handles adding a combo box widget with item names from a specific json file
            :param layout: PyQT layout
            :param label: label name
            :param json: name of the json file
            :param funct: function to connect items to
            :param x: row in layout
            :param y: col in layout
            :param in_line: whether to put the combox in the same row as the label
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

            if in_line:
                layout.addWidget(combo_box, x, y + 1, 1, -1)
            else:
                layout.addWidget(combo_box, x + 1, y, 1, -1)
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
        base_stats_layout.setAlignment(Qt.AlignTop)

        # Add stat function
        def add_stat_to_layout(layout, label, row, signal_function=None, force_int=False, read_only=False):
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
            layout.addWidget(new_label, row, 0)
            layout.addWidget(new_line_edit, row, 2)

            return new_line_edit

        # Tonnage
        base_stats_layout.addWidget(QLabel("Tonnage: "), 0, 0)
        self.tonnage_box = QComboBox()
        for item in get_file_data("hull_data.json").values():
            tonnage = str(item.get('tonnage'))
            self.tonnage_box.addItem(tonnage)
        self.tonnage_box.activated.connect(self.edit_tonnage)
        base_stats_layout.addWidget(self.tonnage_box, 0, 2)

        # Cargo
        self.cargo_line_edit = add_stat_to_layout(base_stats_layout, "Cargo:", 1, read_only=True)

        # Fuels
        self.fuel_line_edit = add_stat_to_layout(base_stats_layout, "Fuel:", 2,
                                                 signal_function=self.edit_fuel, force_int=True)
        self.fuel_line_edit.validator().setBottom(0)

        # Fuel to jump
        self.fuel_label = add_stat_to_layout(base_stats_layout, "Fuel/Jump:", 3, read_only=True)

        # Jump
        base_stats_layout.addWidget(QLabel(""), 4, 0)
        self.jump_line_edit = add_stat_to_layout(base_stats_layout, "Jump:", 5, signal_function=self.edit_jdrive)
        self.jump_label = QLabel("-")
        base_stats_layout.addWidget(self.jump_label, 5, 1)

        # Thrust
        self.thrust_line_edit = add_stat_to_layout(base_stats_layout, "Thrust:", 6, signal_function=self.edit_mdrive)
        self.thrust_label = QLabel("-")
        base_stats_layout.addWidget(self.thrust_label, 6, 1)

        # PPlant
        self.pplant_line_edit = add_stat_to_layout(base_stats_layout, "PPlant:", 7, signal_function=self.edit_pplant)
        self.pplant_label = QLabel("-")
        base_stats_layout.addWidget(self.pplant_label, 7, 1)

        # Hull HP
        base_stats_layout.addWidget(QLabel(""), 8, 0)
        self.hull_hp_line_edit = add_stat_to_layout(base_stats_layout, "Hull HP:", 9,
                                                    signal_function=self.edit_tonnage, read_only=True)

        # Structure HP
        self.structure_hp_line_edit = add_stat_to_layout(base_stats_layout, "Structure HP:", 10,
                                                         signal_function=self.edit_tonnage, read_only=True)

        # Armor
        self.armour_line_edit = add_stat_to_layout(base_stats_layout, "Armour:", 11, read_only=True)

        # Adding discount field
        base_stats_layout.addWidget(QLabel(""), 12, 0)
        self.discount = add_stat_to_layout(base_stats_layout, "Discount %:", 13, force_int=True,
                                           signal_function=self.edit_discount)
        self.discount.validator().setBottom(0)
        self.discount.validator().setTop(100)

        # Cost
        self.cost_line_edit = add_stat_to_layout(base_stats_layout, "Cost (MCr.):", 14, read_only=True)

        # Grid layout
        base_stats_group.setLayout(base_stats_layout)
        ###################################
        ###  END: Base Stats Grid       ###
        ###################################

        ###################################
        ###  START: Armor/Config Grid   ###
        ###################################
        self.armor_scroll = QScrollArea()
        self.armor_config_group = QGroupBox("Config/Armor")
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

        ### Fuel Options ###
        self.armor_config_layout.addWidget(QLabel("Fuel Options:"), 3, 1)

        # Fuel Scoop
        self.fuel_scoop = add_hull_option(self.armor_config_layout, "Fuel Scoop",
                                          lambda: self.modify_fuel_scoops(), 4, 1)

        ### Hull config list ###
        self.hull_config_box = add_combo_box(self.armor_config_layout, "Hull Config: ",
                                             "hull_config.json", self.edit_hull_config, 5, 0)

        ### Sensors ###
        self.sensors = add_combo_box(self.armor_config_layout, "Sensors: ", "hull_sensors.json",
                                     self.edit_sensors, 7, 0)

        ### Armor list ###
        self.armor_combo_box = add_combo_box(self.armor_config_layout, "Armour:",
                                             "hull_armor.json", self.edit_armor, 9, 0, in_line=False, null_spot=True)

        ### Scroll area properties ###
        self.armor_scroll.setFrameShape(QFrame.NoFrame)
        self.armor_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.armor_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.armor_scroll.setWidgetResizable(True)

        self.armor_config_group.setLayout(self.armor_config_layout)
        self.armor_scroll.setWidget(self.armor_config_group)
        ###################################
        ###  END: Armor/Config Grid     ###
        ###################################

        ###################################
        ###  START: Computer Grid       ###
        ###################################
        self.computer_config_group = QGroupBox("Computer")
        self.computer_config_layout = QGridLayout()
        self.computer_config_layout.setAlignment(Qt.AlignTop)

        # Computer Model
        self.computers = add_combo_box(self.computer_config_layout, "Model: ", "hull_computer.json",
                                       self.edit_computer, 2, 0, null_spot=True)

        # Computer Rating
        self.computer_config_layout.addWidget(QLabel("Rating:"), 4, 0)
        self.rating = QLabel("--/--")
        self.computer_config_layout.addWidget(self.rating, 4, 1)
        self.computer_config_layout.addWidget(QLabel(""), 5, 0)

        # Computer customizations
        self.computer_config_layout.addWidget(QLabel("Customizations:"), 6, 0)

        self.jump_control_spec = add_hull_option(self.computer_config_layout, "Jump Control Spec",
                                                 lambda: self.modify_computer_addon("Jump Control Spec"), 7, 0)

        self.hardened_system = add_hull_option(self.computer_config_layout, "Hardened System",
                                               lambda: self.modify_computer_addon("Hardened System"), 8, 0)

        self.computer_config_layout.addWidget(QLabel(""), 9, 0)

        # Software
        self.computer_config_layout.addWidget(QLabel("Software:"), 10, 0)
        self.software_box = QComboBox()
        self.software_box.addItem("---")
        for item in get_file_data("hull_software.json").keys():
            self.software_box.addItem(item)
        button = QPushButton("Add")
        button.clicked.connect(lambda: self.add_software(self.software_box))
        self.computer_config_layout.addWidget(self.software_box, 11, 0)
        self.computer_config_layout.addWidget(QLabel(), 11, 1)
        self.computer_config_layout.addWidget(button, 11, 2)

        # Occupied rows for software placement
        self.software_num_rows = 12

        self.computer_config_group.setLayout(self.computer_config_layout)
        ###################################
        ###  END: Computer Grid         ###
        ###################################

        ###################################
        ###  START: Misc Items Grid     ###
        ###################################
        self.misc_scroll = QScrollArea()
        self.misc_config_group = QGroupBox("Living/Vehicles/Drones")
        self.misc_config_layout = QGridLayout()
        self.misc_config_layout.setAlignment(Qt.AlignTop)

        # Combobox of misc items with dict relating to index position
        self.misc_dict = {}
        idx = 1
        self.misc_box = QComboBox()
        self.misc_box.addItem(" ")
        for item in get_file_data("hull_misc.json").keys():
            self.misc_dict[item] = idx
            self.misc_box.addItem(item)
            idx += 1

        # Button that triggers the add
        button = QPushButton("Add")
        button.clicked.connect(lambda: self.add_misc(self.misc_box))

        # Adding elements to GUI
        self.misc_config_layout.addWidget(self.misc_box, 0, 0)
        self.misc_config_layout.addWidget(QLabel(), 0, 1)
        self.misc_config_layout.addWidget(button, 0, 2)
        self.misc_num_rows = 1

        # Setting scroll area properties
        self.misc_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.misc_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.misc_scroll.setWidgetResizable(True)
        self.misc_scroll.setFrameShape(QFrame.NoFrame)

        self.misc_config_group.setLayout(self.misc_config_layout)
        self.misc_scroll.setWidget(self.misc_config_group)
        ###################################
        ###  END: Misc Items Grid       ###
        ###################################

        ###################################
        ###  START: HP Stats Grid       ###
        ###################################
        self.hpstats_config_group = QGroupBox("Hardpoint Stats:")
        self.hpstats_config_layout = QGridLayout()
        self.hpstats_config_layout.setAlignment(Qt.AlignTop)

        def add_turret_stat(layout, row, string):
            # Handles creating and adding a name and value to a layout
            name_label = QLabel(string)
            value_label = QLabel("0")

            layout.addWidget(name_label, row, 0)
            layout.addWidget(value_label, row, 1)
            return name_label, value_label

        _, self.active_hardpoints = add_turret_stat(self.hpstats_config_layout, 0, "Active HPs:")
        _, self.hardpoint_cost = add_turret_stat(self.hpstats_config_layout, 1, "Cost: ")
        _, self.hardpoint_ton = add_turret_stat(self.hpstats_config_layout, 2, "Tonnage: ")

        """ Showing how many of each turret model """
        self.hpstats_config_layout.addWidget(QLabel(""), 3, 0)
        self.hpstats_config_layout.addWidget(QLabel("Turret Models:"), 4, 0)

        self.model_dict = dict()
        row = 5
        for model in get_file_data("hull_turrets.json").get("models").keys():
            name, value = add_turret_stat(self.hpstats_config_layout, row, model)
            self.model_dict[model] = value
            row += 1

        self.hpstats_config_group.setLayout(self.hpstats_config_layout)
        ###################################
        ###  END: HP Stats Grid         ###
        ###################################
        self.hpstats2_config_group = QGroupBox("Cont.")
        self.hpstats2_config_layout = QGridLayout()
        self.hpstats2_config_layout.setAlignment(Qt.AlignTop)

        """ Showing how much of each weapon """
        self.hpstats2_config_layout.addWidget(QLabel("Weapons:"), row + 1, 0)

        row += 2
        self.weapon_dict = dict()
        for weapon in get_file_data("hull_turrets.json").get("weapons").keys():
            name, value = add_turret_stat(self.hpstats2_config_layout, row, weapon)
            self.weapon_dict[weapon] = value
            row += 1

        self.hpstats2_config_layout.addWidget(QLabel(""), row, 0)
        self.hpstats2_config_layout.addWidget(QLabel("Bay Weapons:"), row + 1, 0)
        row += 2

        self.bay_dict = dict()
        for weapon in get_file_data("hull_turrets.json").get("bayweapons").keys():
            name, value = add_turret_stat(self.hpstats2_config_layout, row, weapon)
            self.bay_dict[weapon] = value
            row += 1

        self.hpstats2_config_group.setLayout(self.hpstats2_config_layout)
        ###################################
        ###  START: Hardpoint Grid      ###
        ###################################
        self.hp_scroll = QScrollArea()
        self.hp_config_group = QGroupBox("Hardpoints:")
        self.hp_config_layout = QGridLayout()
        self.hp_config_layout.setAlignment(Qt.AlignTop)

        # Total and available hardpoints
        self.hp_config_layout.addWidget(QLabel("Total: "), 0, 0)
        self.total_hp = QLabel(str(self.spacecraft.num_hardpoints))
        self.hp_config_layout.addWidget(self.total_hp, 0, 1)

        self.hp_config_layout.addWidget(QLabel("Avail: "), 0, 2)
        self.avail_hp = QLabel(str(self.spacecraft.num_hardpoints - len(self.spacecraft.hardpoints)))
        self.hp_config_layout.addWidget(self.avail_hp, 0, 3)

        # Add button connecting to adding a hardpoint
        add_hp = QPushButton("Add")
        add_hp.setMaximumWidth(30)
        add_hp.clicked.connect(self.add_hardpoint)
        self.hp_config_layout.addWidget(add_hp, 0, 4)

        # Global list to hold active button objects
        self.active_hp_buttons = list()
        self.active_hp_id = None

        # Setting properties of scroll area
        self.hp_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.hp_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.hp_scroll.setWidgetResizable(True)
        self.hp_scroll.setFrameShape(QFrame.NoFrame)

        self.hp_config_group.setLayout(self.hp_config_layout)
        self.hp_scroll.setWidget(self.hp_config_group)
        ###################################
        ###  END: Hardpoint Grid        ###
        ###################################

        ###################################
        ###  START: Turret Grid         ###
        ###################################
        self.turret_config_group = QGroupBox("Active Turret:")
        self.turret_config_layout = QGridLayout()
        self.turret_config_layout.setAlignment(Qt.AlignTop)

        self.turret_config_group.setLayout(self.turret_config_layout)
        ###################################
        ###  END: Turret Grid           ###
        ###################################

        # Checking bridge to true, needed after initializing everything
        self.bridge_check.setChecked(True)

        # Setting initial discount to 0%
        self.discount.setText("0")
        self.edit_discount()

        # Setting appropriate column widths
        FIXED_WIDTH = 250
        base_stats_group.setFixedWidth(175)
        self.hpstats_config_group.setFixedWidth(175)

        self.armor_config_group.setFixedWidth(FIXED_WIDTH)
        self.computer_config_group.setFixedWidth(FIXED_WIDTH)
        self.misc_config_group.setFixedWidth(FIXED_WIDTH)
        self.misc_scroll.setFixedWidth(FIXED_WIDTH)

        self.hpstats2_config_group.setFixedWidth(FIXED_WIDTH)
        self.hp_config_group.setFixedWidth(FIXED_WIDTH)
        self.hp_scroll.setFixedWidth(FIXED_WIDTH)
        self.turret_config_group.setFixedWidth(FIXED_WIDTH)

        # Setting appropriate layout heights
        FIXED_HEIGHT = 400
        base_stats_group.setFixedHeight(FIXED_HEIGHT)
        self.computer_config_group.setFixedHeight(FIXED_HEIGHT)
        self.turret_config_group.setFixedHeight(350)

        # Overall layout grid
        # Top row
        layout = QGridLayout()
        layout.addWidget(base_stats_group, 0, 0)
        layout.addWidget(self.armor_scroll, 0, 1)
        layout.addWidget(self.computer_config_group, 0, 2)
        layout.addWidget(self.misc_scroll, 0, 3)
        # Second Row
        layout.addWidget(self.hpstats_config_group, 1, 0)
        layout.addWidget(self.hpstats2_config_group, 1, 1)
        layout.addWidget(self.hp_scroll, 1, 2)
        layout.addWidget(self.turret_config_group, 1, 3)

        # Setting layout to be the central widget of main window
        wid = QWidget()
        wid.setLayout(layout)
        self.setCentralWidget(wid)

        # Update to current stats
        self.update_stats()

    def open_file(self):
        """
        # Handles the QtFileDialog for loading in ship formats
        """
        dlg = QFileDialog()

        # Doing the interaction
        filename = dlg.getOpenFileName(self, 'Load File', 'shipyard/models/', 'Traveller SRD files (*.srd)')

        if filename[0] != '':
            self.setWindowTitle("Imperium Shipyard - {}".format(filename[0].split('/')[-1]))
            self.fileloader.load_model(filename[0], self)

    def save_file(self):
        """
        Handles the QtFileDialog for saving the current ship to a file
        """
        dlg = QFileDialog()

        # Doing the interaction
        filename = dlg.getSaveFileName(self, 'Save File', 'shipyard/models', 'Traveller SRD files (*.srd)')

        if filename[0] != '':
            self.setWindowTitle("Imperium Shipyard - {}".format(filename[0].split('/')[-1]))
            self.fileloader.save_model(filename[0], self.spacecraft)

    def reset_ship(self):
        """
        Handles getting the path to the default SRD file and resetting the GUI to a default ship
        """
        my_path = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(my_path, "imperium/shipyard/models/default/default.srd")

        self.setWindowTitle("Imperium Shipyard - Untitled.srd")
        self.fileloader.load_model(filename, self)

    def update_stats(self):
        """
        Updates the UI with the current Spacecraft stats
        """
        self.cargo_line_edit.setText(str(        self.spacecraft.get_remaining_cargo()))
        self.fuel_line_edit.setText(str(         self.spacecraft.fuel_max           ))
        self.fuel_label.setText(str(             self.spacecraft.fuel_jump          ))
        self.jump_line_edit.setText(str(         self.spacecraft.jump               ))
        self.thrust_line_edit.setText(str(       self.spacecraft.thrust             ))
        self.pplant_line_edit.setText(str(       self.spacecraft.fuel_two_weeks     ))
        self.hull_hp_line_edit.setText(str(      self.spacecraft.hull_hp            ))
        self.structure_hp_line_edit.setText(str( self.spacecraft.structure_hp       ))
        self.armour_line_edit.setText(str(       self.spacecraft.armour_total       ))
        self.cost_line_edit.setText("{:0.3f}".format(self.spacecraft.get_total_cost()))

        # Updating the hardpoint stats information
        self.update_turret_stats()

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

        # Update computer rating
        total_rating = "0" if self.spacecraft.computer is None else self.spacecraft.computer.rating
        self.rating.setText("{}/{}".format(self.spacecraft.check_rating_ratio(), total_rating))

    def update_turret_stats(self):
        """
        Updates turret column stats with appropriate
        """
        self.active_hardpoints.setText(str(len(self.spacecraft.hardpoints)))

        # Updating the number of turrets per model
        turret_dict = dict()
        for model in get_file_data("hull_turrets.json").get("models").keys():
            turret_dict[model] = 0

        for hardpoint in self.spacecraft.hardpoints:
            if hardpoint.turret is not None:
                name = hardpoint.turret.name
                turret_dict[name] = turret_dict.get(name) + 1

        for model in turret_dict.keys():
            self.model_dict[model].setText(str(turret_dict.get(model)))

        # Updating the number of turret weapons
        wep_dict = dict()
        for model in get_file_data("hull_turrets.json").get("weapons").keys():
            wep_dict[model] = 0

        for hardpoint in self.spacecraft.hardpoints:
            if hardpoint.turret is not None:
                for wep in hardpoint.turret.weapons:
                    if wep is not None and hardpoint.turret.name != "Bay Weapon":
                        name = wep.get("name")
                        wep_dict[name] = wep_dict.get(name) + 1

        for weapon in wep_dict.keys():
            self.weapon_dict[weapon].setText(str(wep_dict.get(weapon)))

        # Updating the number of bay weapons
        wep_dict = dict()
        for model in get_file_data("hull_turrets.json").get("bayweapons").keys():
            wep_dict[model] = 0

        for hardpoint in self.spacecraft.hardpoints:
            if hardpoint.turret is not None:
                for wep in hardpoint.turret.weapons:
                    if wep is not None and hardpoint.turret.name == "Bay Weapon":
                        name = wep.get("name")
                        wep_dict[name] = wep_dict.get(name) + 1

        for weapon in wep_dict.keys():
            self.bay_dict[weapon].setText(str(wep_dict.get(weapon)))

        # Setting current total cost and tonnage
        cost = 0
        tonnage = 0
        for hardpoint in self.spacecraft.hardpoints:
            cost += hardpoint.get_cost()
            tonnage += hardpoint.get_tonnage()
        self.hardpoint_cost.setText(str(round(cost, 2)))
        self.hardpoint_ton.setText(str(tonnage))

    def edit_tonnage(self):
        """
        Update the spacecraft tonnage
        Updates the Drives to the lowest available type at that tonnage level
        """
        new_tonnage = int(self.tonnage_box.currentText())

        # Return if the tonnage is the same
        if new_tonnage == self.spacecraft.tonnage:
            return

        # Set tonnage on the spacecraft object
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

        # Update hardpoint counter
        self.total_hp.setText(str(self.spacecraft.num_hardpoints))
        self.avail_hp.setText(str(self.spacecraft.num_hardpoints - len(self.spacecraft.hardpoints)))

        # Update stats
        self.update_stats()

    def edit_discount(self):
        """
        Update the discount factor of the ship
        """
        val = int(self.discount.text())
        self.spacecraft.set_discount(val)
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
        self.update_stats()

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
        self.update_stats()

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
        self.update_stats()

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
            self.display_armor()
            return

        # Creating new armor object and adding to ship
        armor = Armour(armor_type)
        self.spacecraft.add_armour(armor)

        # Button to handle removing the piece of armor
        self.display_armor()

    def remove_armor(self, armor):
        """
        Handles removing a piece of armor from the ship, as well as updating GUI to reflect changes
        :param armor: armour object to remove
        """
        self.spacecraft.remove_armour(armor)
        self.display_armor()

    def display_armor(self):
        """ Handles clearing out the armor column and recreating their buttons """

        # Clearing out old weapons
        for i in reversed(range(16, self.armor_config_layout.count())):
            self.armor_config_layout.itemAt(i).widget().setParent(None)

        # Loop through current armor and making new buttons
        for armor in self.spacecraft.armour:
            button = QPushButton()
            button.setCheckable(True)
            button.setText("{} - Protect: {}".format(armor.type, armor.protection))
            self.connect_armor(armor, button)
            self.armor_config_layout.addWidget(button, self.armor_config_layout.count(), 0, 1, -1)

        self.update_stats()

    def connect_armor(self, armor, button):
        """ Helper function for the lambda button connections"""
        button.clicked.connect(lambda: self.remove_armor(armor))
        button.clicked.connect(button.deleteLater)

    def edit_hull_config(self):
        """
        Handles editing the hull config with a new one, adjusting the GUI and values
        """
        text = self.hull_config_box.currentText()
        config = Config(text)
        self.spacecraft.edit_hull_config(config)

        # Distributed hulls can't have fuel scoops
        if config.type == "Distributed":
            self.fuel_scoop.setDisabled(True)
        else:
            self.fuel_scoop.setEnabled(True)

        # Streamlined hulls have scoops built in. Set fuel scoops to unchecked on config swap
        if config.type == "Streamlined":
            self.fuel_scoop.setChecked(True)
        else:
            self.fuel_scoop.setChecked(False)

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

    def edit_sensors(self):
        # Handles adding sensor suite to ships
        sensor_type = self.sensors.currentText()
        sensor = Sensor(sensor_type)

        self.spacecraft.add_sensors(sensor)
        self.update_stats()

    """ COMPUTER/SOFTWARE FUNCTIONS """
    def edit_computer(self):
        # Handles adding/removing computers to a ship
        computer_type = self.computers.currentText()

        # Checking for whether the computer was removed or not
        if computer_type == "---":
            computer = None
        else:
            computer = Computer(computer_type)

        # Uncheck customization options
        self.jump_control_spec.setChecked(False)
        self.hardened_system.setChecked(False)

        # Adding computer to ship, updating stats
        self.spacecraft.add_computer(computer)
        self.update_stats()

    def modify_computer_addon(self, name):
        # Handles modifying the spacecraft's computer addon
        if self.spacecraft.computer is not None:
            self.spacecraft.computer.modify_addon(name)
        self.update_stats()

    def add_software(self, box):
        """
        Handles adding new software to the GUI
        :param box: software box of the GUI, self.software_box
        """
        # If there are no items left
        if box.count() == 0 or box.currentText() == "---":
            return

        # Get software to add and add base level to ship
        software_name = box.currentText()
        base_level = float('inf')
        for level in get_file_data("hull_software.json").get(software_name).keys():
            if level != "mod_additional":
                if int(level) < base_level:
                    base_level = int(level)

        software = Software(software_name, base_level)
        self.spacecraft.modify_software(software)

        # Remove software from combobox
        box.removeItem(box.currentIndex())
        box.setCurrentIndex(0)

        # Add ship, display software, update stats
        self.display_software()
        self.update_stats()

    def remove_software(self, label):
        """
        Handles removing the GUI elements on "Remove" button click
        :param label: QLabel of that row
        """
        software_name = label.text()
        self.spacecraft.remove_software(software_name)

        # Redisplay software
        self.display_software()

        # Adding item back to combobox
        self.software_box.addItem(software_name)
        self.update_stats()

    def display_software(self):
        """ Handles clearing and redisplaying the GUI elements """
        # Clearing out software column
        for i in reversed(range(13, self.computer_config_layout.count())):
            self.computer_config_layout.itemAt(i).widget().setParent(None)

        # Loops through active software and creates GUI elements for them
        for software in self.spacecraft.software:
            software_name = software.type

            # GUI elements for newly added software
            software_label = QLabel(software_name)
            software_combobox = QComboBox()
            software_button = QPushButton("Remove")

            # Connect software func
            self.connect_software_func(software, software_combobox, software_name, software_label, software_button)

            # Adding widgets to GUI
            count = self.computer_config_layout.count()
            self.computer_config_layout.addWidget(software_label, count, 0)
            self.computer_config_layout.addWidget(software_combobox, count, 1)
            self.computer_config_layout.addWidget(software_button, count, 2)

    def connect_software_func(self, software, combobox, name, label, button):
        """ Helper function to connect lambdas to GUI """
        # Build the combobox
        for item in get_file_data("hull_software.json").get(name):
            if item != "mod_additional":
                combobox.addItem(item)

        # Set currentText to level of the software and connect combobox functionality
        combobox.setCurrentText(str(software.level))
        self.connect_software_modify(combobox, name, label)

        # Button functionality
        button.clicked.connect(lambda: self.remove_software(label))
        button.clicked.connect(label.deleteLater)
        button.clicked.connect(combobox.deleteLater)
        button.clicked.connect(button.deleteLater)

    def connect_software_modify(self, combobox, name, label):
        """ Helper to the helper for connecting the software level combobox """
        combobox.currentTextChanged.connect(lambda: self.modify_software_level(label, combobox))

    def modify_software_level(self, label, box):
        """
        Modifies the level of an already added software piece, removing if the level is '-'
        :param label: QLabel of that row
        :param box: QComboBox of that software
        """
        # Get software name/level
        software_level = box.currentText()
        software_name = label.text()

        # Create software, add it to ship
        software = Software(software_name, software_level)
        self.spacecraft.modify_software(software)

        self.update_stats()

    """ MISC FUNCTIONS """
    def add_misc(self, box):
        """
        Handles adding new misc items to the GUI
        :param box: misc box of the GUI, self.misc_box
        """
        # If there are no items left or trying to add invalid item
        invalids = [" ", "--- Living ---", "--- Vehicles ---", "--- Drones ---"]
        if box.count() == 0 or box.currentText() in invalids:
            return

        # Removing item from misc list, adding to ship
        misc_name = box.currentText()
        box.removeItem(box.currentIndex())
        self.spacecraft.modify_misc(Misc(misc_name, 1))

        # Display misc items, set box index to 0
        self.display_misc_items()
        self.misc_box.setCurrentIndex(0)
        self.misc_num_rows += 1
        self.update_stats()

    def remove_misc(self, label):
        """
        Handles removing the misc item from the GUI on button click
        :param label: QLabel
        """
        misc_name = label.text()

        # Remove item from spacecraft
        self.spacecraft.remove_misc(misc_name)

        # Redisplay misc items
        self.display_misc_items()

        # Adding item back to combobox, checking for index placement
        count_before_misc = 0
        for item in self.spacecraft.misc:
            if self.misc_dict.get(item.name) < self.misc_dict.get(misc_name):
                count_before_misc += 1

        idx = self.misc_dict.get(misc_name) - count_before_misc
        self.misc_box.insertItem(idx, misc_name)
        self.update_stats()

    def modify_misc_item(self, label, line):
        """
        Handles altering the spacecraft with updated misc item on item change
        :param label: QLabel of misc item
        :param line: QLineEdit, quantity of item
        """
        name = label.text()
        num_misc = line.text()

        # Create item, add to ship
        misc = Misc(name, int(num_misc))
        self.spacecraft.modify_misc(misc)
        self.update_stats()

    def display_misc_items(self):
        """ Function that handles redisplaying all of the misc GUI elements on the ship """

        # Clearing out misc column
        for i in reversed(range(3, self.misc_config_layout.count())):
            self.misc_config_layout.itemAt(i).widget().setParent(None)

        # Looping through misc and adding gui elements
        for misc in self.spacecraft.misc:
            # Making GUI elements
            label = QLabel(misc.name)

            line_edit = QLineEdit()
            line_edit.setFixedWidth(25)
            line_edit.setValidator(QIntValidator(line_edit))
            line_edit.validator().setBottom(0)
            line_edit.setText(str(misc.num))

            button = QPushButton("Remove")

            # Connecting functionality
            self.connect_misc_item(label, line_edit, button)

            # Adding widgets to GUI
            count = self.misc_config_layout.count()
            self.misc_config_layout.addWidget(label, count, 0)
            self.misc_config_layout.addWidget(line_edit, count, 1)
            self.misc_config_layout.addWidget(button, count, 2)

    def connect_misc_item(self, label, line_edit, button):
        """ Helper function that handle connecting the lambda functions for GUI elements """
        line_edit.editingFinished.connect(lambda: self.modify_misc_item(label, line_edit))
        button.clicked.connect(lambda: self.remove_misc(label))
        button.clicked.connect(label.deleteLater)
        button.clicked.connect(line_edit.deleteLater)
        button.clicked.connect(button.deleteLater)

    def modify_fuel_scoops(self):
        # Flips the fuel scoop box
        self.spacecraft.modify_fuel_scoops()
        self.update_stats()

    """ HARDPOINT/TURRET FUNCTIONS """
    def add_hardpoint(self):
        """
        Handles adding a hardpoint to the ship with an arrow to modify turret options
        """
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        hardpoint = Hardpoint(name)

        # Add hardpoint to ship, redisplay all hardpoints
        self.spacecraft.add_hardpoint(hardpoint)
        self.display_hardpoints()

        # Update stats
        self.avail_hp.setText(str(self.spacecraft.num_hardpoints - len(self.spacecraft.hardpoints)))
        self.update_stats()

    def remove_hardpoint(self, hardpoint):
        """
        Handles the functionality of removing a single hardpoint from the ship and GUI
        :param hardpoint: hardpoint class
        :param active: button to display information
        """
        # Wipe out turret layout if removed turret is displayed
        if hardpoint.id == self.active_hp_id:
            for i in reversed(range(self.turret_config_layout.count())):
                self.turret_config_layout.itemAt(i).widget().setParent(None)

        # Remove hardpoint from ship, redisplay hardpoints
        self.spacecraft.remove_hardpoint(hardpoint)
        self.display_hardpoints()

        # Update stats
        self.avail_hp.setText(str(self.spacecraft.num_hardpoints - len(self.spacecraft.hardpoints)))
        self.update_stats()

    def display_hardpoints(self):
        """
        Handles looping through hardpoints on ship and remaking the pyQT GUI elements for them
        Remakes the active HP buttons list for turret window displaying
        """
        # Clear active hp buttons
        self.active_hp_buttons = list()

        # Clearing out the hardpoint col
        for i in reversed(range(5, self.hp_config_layout.count())):
            self.hp_config_layout.itemAt(i).widget().setParent(None)

        # Loop through hardpoints to display
        for hp in self.spacecraft.hardpoints:
            # Creating GUI elements
            activate = QPushButton("HP {}".format(hp.id))
            if hp.id == self.active_hp_id:
                activate.setDisabled(True)

            remove = QPushButton("X")
            remove.setMaximumWidth(30)

            # Button functionalities
            self.connect_hp_items(remove, hp, activate)

            # Adding to GUI
            self.active_hp_buttons.append(activate)
            count = self.hp_config_layout.count()
            self.hp_config_layout.addWidget(activate, count, 0, 1, 4)
            self.hp_config_layout.addWidget(remove, count, 4)

    def connect_hp_items(self, remove, hardpoint, activate):
        """ Helper function that handles connecting hardpoint to its functions """
        remove.clicked.connect(lambda: self.remove_hardpoint(hardpoint))
        remove.clicked.connect(remove.deleteLater)
        remove.clicked.connect(activate.deleteLater)
        activate.clicked.connect(lambda: self.display_turret(self.turret_config_layout, activate, hardpoint))

    def display_turret(self, layout, active, hardpoint):
        """
        Handles displaying a hardpoint's information and updating the active buttons
        :param active: active button to set disabled
        :param hardpoint: hardpoint holding a turret to display
        """
        # Handle updating active button id and which is disabled
        for button in self.active_hp_buttons:
            if button is active:
                button.setDisabled(True)
            else:
                button.setEnabled(True)

        self.active_hp_id = hardpoint.id

        # Clear the previous layout
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        """ Displaying hardpoint/turret information """
        label = QLabel("---- HP: {} ----".format(str(hardpoint.id)))
        layout.addWidget(label, 0, 0)

        # Combobox for turret model on hardpoint
        turret_label = QLabel("Turret Model:")
        turret_box = QComboBox()
        turret_box.addItem("---")
        idx = 1
        for key in get_file_data("hull_turrets.json").get("models").keys():
            turret_box.addItem(key)
            if hardpoint.turret is not None and hardpoint.turret.name == key:
                turret_box.setCurrentIndex(idx)
            idx += 1

        turret_box.currentTextChanged.connect(lambda: self.modify_turret_model(layout, hardpoint, turret_box))
        layout.addWidget(turret_label, 1, 0)
        layout.addWidget(turret_box, 2, 0, 1, -1)

        if turret_box.currentText() == "Bay Weapon":
            # Check if hardpoint has a bayweapon
            self.display_bayweapons(layout, hardpoint)
        else:
            # Displaying turret wep information
            self.display_turret_weps(layout, hardpoint)

    def display_turret_weps(self, layout, hardpoint):
        """
        Handles displaying the weapons for a turret
        :param layout: PyQT Grid Layout to add to
        :param hardpoint: hardpoint object with turret
        """
        # Clearing out old weapons
        for i in reversed(range(3, layout.count())):
            layout.itemAt(i).widget().setParent(None)

        # Add turret options
        self.add_turret_options(layout, hardpoint)

        # If turret is None, don't display weps
        if hardpoint.turret is None:
            return

        # Creating objects to display weapons
        row = 4
        for idx in range(hardpoint.turret.max_wep):
            label, combobox = self.add_turret_weapon(idx, hardpoint)
            layout.addWidget(label, row + idx, 0)
            layout.addWidget(combobox, row + idx, 1, 1, -1)

        # Adding missiles to GUI
        row = self.add_turret_missiles(layout, hardpoint)

        # Sandcaster barrels
        label = QLabel("Sandcaster Barrels:")
        total_label, edit = self.add_turret_ammo(hardpoint, "Sandcaster")
        layout.addWidget(label, row, 0)
        layout.addWidget(total_label, row, 1)
        layout.addWidget(edit, row, 2)

    def display_bayweapons(self, layout, hardpoint):
        """
        Handles the display path for bayweapons and syncing up the functions to handle that
        :param layout: PyQT layout to put new widgets in
        :param hardpoint: hardpoint object to interact with
        """
        # Clearing out old weapons
        for i in reversed(range(3, layout.count())):
            layout.itemAt(i).widget().setParent(None)

        # Add whitespace for removal
        # for i in range(4):
        #    layout.addWidget(QLabel(), 3, i)

        # Creating combobox for bayweapons
        label = QLabel("Wep:")
        combobox = QComboBox()
        combobox.addItem("---")
        counter = 1
        for key in get_file_data("hull_turrets.json").get("bayweapons").keys():
            combobox.addItem(key)
            if hardpoint.turret.weapons[0] is not None and key == hardpoint.turret.weapons[0].get("name"):
                combobox.setCurrentIndex(counter)
            counter += 1

        combobox.currentTextChanged.connect(
            lambda: self.modify_turret_wep(hardpoint.turret, combobox.currentText(), 0)
        )

        layout.addWidget(label, 5, 0)
        layout.addWidget(combobox, 5, 1, 1, -1)

        # Adding missiles to GUI
        self.add_turret_missiles(layout, hardpoint)

    def add_turret_options(self, layout, hardpoint):
        """
        Support function that handles adding a turret's options in the form of check boxes
        :param layout: PyQT layout to add widgets to
        :param hardpoint: Hardpoint object to interact with
        """
        # Checkboxes for pop-up and fixed mounting
        popup_label = QLabel("Pop-up Cover:")
        popup_check = QCheckBox()
        if hardpoint.popup is True:
            popup_check.setChecked(True)
        popup_check.clicked.connect(lambda: self.modify_turret_option(hardpoint, "Pop-up Turret"))
        layout.addWidget(popup_label, 3, 0)
        layout.addWidget(popup_check, 3, 1)

        fixed_label = QLabel("Fixed Mounting:")
        fixed_check = QCheckBox()
        if hardpoint.fixed is True:
            fixed_check.setChecked(True)
        fixed_check.clicked.connect(lambda: self.modify_turret_option(hardpoint, "Fixed Mounting"))
        layout.addWidget(fixed_label, 3, 2)
        layout.addWidget(fixed_check, 3, 3)

    def add_turret_missiles(self, layout, hardpoint):
        """
        Support function that handles adding the missiles in hull_turrets.json onto a layout and syncing up
        the relevant functions for the line edits
        :param hardpoint: Hardpoint object to interact with
        :param layout: PyQT layout to add widgets to
        :return: updated row at the end
        """
        # Creating objects to display missile ammo and sandcaster barrels
        layout.addWidget(QLabel(""), 7, 0)
        layout.addWidget(QLabel("Turret Ammo:"), 8, 0)
        layout.addWidget(QLabel("#"), 8, 1)
        layout.addWidget(QLabel("Tons"), 8, 2)

        # Missile ammo
        row = 9
        for key in hardpoint.turret.missiles.keys():
            label = QLabel("{} Missiles:".format(key))
            total_label, edit = self.add_turret_ammo(hardpoint, key)
            layout.addWidget(label, row, 0)
            layout.addWidget(total_label, row, 1)
            layout.addWidget(edit, row, 2)
            row += 1

        return row

    def add_turret_weapon(self, idx, hardpoint):
        """
        Helper function that handles creating the label and combobox for a turret weapon, as well
        as setting up the connection function on activation
        :param idx: index of the weapon in array
        :param hardpoint: hardpoint object
        :return: label of weapon and filled combobox
        """
        label = QLabel("Wep {}:".format(idx))
        combobox = QComboBox()
        combobox.addItem("---")
        counter = 1
        for key in get_file_data("hull_turrets.json").get("weapons").keys():
            combobox.addItem(key)
            if hardpoint.turret.weapons[idx] is not None and key == hardpoint.turret.weapons[idx].get("name"):
                combobox.setCurrentIndex(counter)
            counter += 1

        combobox.currentTextChanged.connect(
            lambda: self.modify_turret_wep(hardpoint.turret, combobox.currentText(), idx))
        return label, combobox

    def add_turret_ammo(self, hardpoint, key):
        """
        Handles creating the widgets for a turret ammo, either missile ammo or sandcaster ammo
        :param idx: index of the gridlayout
        :param hardpoint: hardpoint object
        :param key: key object
        :return: QLabel and QLineEdit with connected function
        """
        edit = QLineEdit()
        edit.setValidator(QIntValidator(edit))
        edit.validator().setBottom(0)
        edit.setMaximumWidth(20)

        if key != "Sandcaster":
            total_label = QLabel(str(hardpoint.turret.missiles.get(key) * 12))
            edit.setText(str(hardpoint.turret.missiles.get(key)))
            edit.editingFinished.connect(lambda: self.modify_turret_ammo(hardpoint.turret, key, total_label, edit))
        else:
            total_label = QLabel(str(hardpoint.turret.sandcaster_barrels * 20))
            edit.setText(str(hardpoint.turret.sandcaster_barrels))
            edit.editingFinished.connect(lambda: self.modify_turret_sandcaster(hardpoint.turret, total_label, edit))
        return total_label, edit

    def modify_turret_model(self, layout, hardpoint, box):
        """
        Handles modifying what type of turret a hardpoint has
        :param hardpoint: hardpoint object
        :param box: PyQT ComboBox
        """
        model = box.currentText()
        if model == "---":
            turret = None
            hardpoint.add_turret(turret)
            self.display_turret_weps(layout, hardpoint)
        elif model == "Bay Weapon":
            turret = Turret(model)
            hardpoint.add_turret(turret)
            self.display_bayweapons(layout, hardpoint)
        else:
            turret = Turret(model)
            hardpoint.add_turret(turret)
            self.display_turret_weps(layout, hardpoint)
        self.update_stats()

    def modify_turret_option(self, hardpoint, part):
        # Handles modifying a hardpoint's addon
        hardpoint.modify_addon(part)
        self.update_stats()

    def modify_turret_wep(self, turret, wep, idx):
        # Handles modifying a turret's weapons
        turret.modify_weapon(wep, idx)
        self.update_stats()

    def modify_turret_ammo(self, turret, ammo_type, total_label, edit):
        # Handles modifying a turret's ammo
        num = int(edit.text())
        turret.modify_missile_ammo(ammo_type, num)
        total_label.setText(str(num * 12))
        self.update_stats()

    def modify_turret_sandcaster(self, turret, total_label, edit):
        # Handles modifying a turret's sandcaster
        num = int(edit.text())
        turret.modify_sandcaster_barrel(num)
        total_label.setText(str(num * 20))
        self.update_stats()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    # Different checking needed depending on local build or executable run
    if os.path.exists("IS-logo.png"):
        window.setWindowIcon(QIcon('IS-logo.png'))
    else:
        window.setWindowIcon(QIcon('images/IS-logo.png'))
    window.show()
    sys.exit(app.exec_())