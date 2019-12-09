"""
spacecraft.py

Houses the spacecraft class
"""
from imperium.models.config import Config
from imperium.models.sensors import Sensor
from imperium.models.json_reader import get_file_data


class Spacecraft:
    """
    The Spacecraft, primary class for organizing spaceship data

    :param hull_tonnage: the size of the hull, in tons
    """
    def __init__(self, hull_tonnage):
        self.tonnage            = 0 # total tonnage of ship
        self.discount           = 1 # discount factor for the cost
        self.hull_hp            = 0 # calculated as 1 per 50 tonnage
        self.structure_hp       = 0 # calculated as 1 per 50 tonnage
        self.jump               = 0 # max number of tiles covered in a single jump
        self.thrust             = 0 # max number of G accelerations available
        self.fuel_max           = 0 # amount of fuel tank
        self.fuel_jump          = 0 # amount of fuel required for a jump
        self.fuel_two_weeks     = 0 # amount of fuel required for 2 weeks of operation
        self.armour_total       = 0 # total armour pointage
        self.num_hardpoints     = 0 # total number of hardpoints
        self.hardpoints         = list() # list of added hardpoints
        self.hull_designation   = None   # A, B, C, etc.
        self.hull_type          = None   # steamlined, distributed, standard, etc.
        self.hull_options       = list() # list of hull options installed
        self.fuel_scoop         = False  # whether fuel scoops are installed
        self.bridge             = False  # whether a bridge is installed
        self.jdrive             = None   # jdrive object
        self.mdrive             = None   # mdrive object
        self.pplant             = None   # pplant object
        self.armour             = list() # list of armour objects
        self.sensors            = None   # sensor object
        self.bays               = list() # list of bay objects
        self.screens            = list() # list of screen objects
        self.computer           = None   # computer object
        self.software           = list() # list of installed software
        self.misc               = list() # list of misc items

        # set the tonnage to that given at init
        if hull_tonnage > 2000:
            hull_tonnage = 2000

        self.tonnage = hull_tonnage

        # set hp based on tonnage
        self.hull_hp = self.tonnage // 50
        self.structure_hp = self.tonnage // 50
        self.num_hardpoints = self.tonnage // 100

        # pull hull cost from json, set that
        data = get_file_data("hull_data.json")

        for key in data.keys():
            # iterate through hull sizes for 
            item_tonnage = data.get(key).get("tonnage")
            if self.tonnage <= item_tonnage and (item_tonnage - self.tonnage) < 100:
                self.hull_designation = key

        # set hull type to standard
        self.hull_type = Config("Standard")

        # set sensors to standard
        self.sensors = Sensor("Standard")

    def get_total_cost(self):
        """
        Gets total cost of all objects for the ship
        :return: total cost
        """
        cost_total = 0

        # Tonnage / Bridge
        if self.tonnage != 0:
            ton = get_file_data("hull_data.json")
            cost = ton.get(self.hull_designation).get("cost")
            cost_total += cost * self.hull_type.mod_hull_cost
        if self.bridge is True:
            cost_total += self.tonnage * .005

        # Hull options
        for opt in self.hull_options:
            cost_total += self.tonnage * opt.cost_per_hull_ton

        # Fuel scoops
        if self.hull_type.type != "Streamlined" and self.fuel_scoop is True:
            cost_total += 1

        # Drives
        if self.jdrive is not None:
            cost_total += self.jdrive.cost
        if self.mdrive is not None:
            cost_total += self.mdrive.cost
        if self.pplant is not None:
            cost_total += self.pplant.cost

        # Armour
        for armour_item in self.armour:
            percent = armour_item.cost_by_hull_percentage
            ton = get_file_data("hull_data.json")
            cost = ton.get(self.hull_designation).get("cost")
            cost_total += percent * cost

        # Sensors
        if self.sensors is not None:
            cost_total += self.sensors.cost

        # Screens / Computer / Software
        for screen in self.screens:
            cost_total += screen.cost
        if self.computer is not None:
            cost_total += self.computer.get_cost()
        for software in self.software:
            cost_total += software.cost

        # Misc
        for misc in self.misc:
            if misc.name == "Repair Drones":
                cost_total += misc.cost * misc.tonnage * self.tonnage
            else:
                cost_total += misc.cost


        # Adding discount to items
        cost_total *= self.discount

        # Turrets / Bayweapons (after discount because its included
        for hardpoint in self.hardpoints:
            cost_total += hardpoint.get_cost()

        return cost_total

    def get_remaining_cargo(self):
        """
        Calculates the remaining cargo for the ship
        :return: Remaining cargo number
        """
        cargo = self.tonnage

        # Fuel / Bridge
        if self.bridge is True:
            cargo -= self.get_bridge_tonnage()
        cargo -= self.fuel_max

        # Drives / PPlant
        if self.jdrive is not None:
            cargo -= self.jdrive.tonnage
        if self.mdrive is not None:
            cargo -= self.mdrive.tonnage
        if self.pplant is not None:
            cargo -= self.pplant.tonnage

        # Armour
        for armour_item in self.armour:
            hull_amount = armour_item.hull_amount
            cargo -= int(self.tonnage * hull_amount)

        # Sensors
        if self.sensors is not None:
            cargo -= self.sensors.tonnage

        # Turrets / Bayweapons / Screens
        for hardpoint in self.hardpoints:
            cargo -= hardpoint.get_tonnage()
        for screen in self.screens:
            cargo -= screen.tonnage

        # Misc
        for misc in self.misc:
            if misc.name == "Repair Drones":
                cargo -= misc.tonnage * self.tonnage
            else:
                cargo -= misc.tonnage

        return round(cargo, 2)

    def set_tonnage(self, new_tonnage):
        """
        Sets the tonnage of an existing Spacecraft
        :param new_tonnage: The tonnage to update to
        """
        tonnage_cost_data = get_file_data("hull_data.json")
        for key in tonnage_cost_data:
            item = tonnage_cost_data.get(key)
            if item.get('tonnage') == int(new_tonnage):
                self.hull_designation = key

        self.tonnage = new_tonnage

        # set hp based on tonnage
        self.hull_hp = self.tonnage // 50
        self.structure_hp = self.tonnage // 50
        self.num_hardpoints = self.tonnage // 100

    def set_discount(self, discount):
        self.discount = (100 - discount) / 100

    def set_fuel(self, new_fuel):
        """
        Sets the max fuel of an existing Spacecraft
        :param new_fuel: The fuel to update to
        """
        self.fuel_max = new_fuel

    def add_jdrive(self, drive):
        """
        Adds a jump drive to the spaceship
        :param drive_type: The drive designation letter
        """
        if self.tonnage == 0:
            return "Error: Tonnage not set before adding j-drive."

        # Error checking to see if new drive type is incompatible
        if self.performance_by_volume("jdrive", drive.drive_type) is None:
            return "Error: non-compatible drive to tonnage value - Drive {} to {}".format(drive.drive_type, self.tonnage)

        self.jdrive = drive
        self.fuel_jump = int(0.1 * self.tonnage * self.jump)

    def add_mdrive(self, drive):
        """
        Adds a maneuver drive to the spaceship
        :param drive_type: The drive designation letter
        """
        if self.tonnage == 0:
            return "Error: Tonnage not set before adding m-drive."

        # Error checking to see if new drive type is incompatible
        if self.performance_by_volume("mdrive", drive.drive_type) is None:
            return "Error: non-compatible drive to tonnage value - Drive {} to {}".format(drive.drive_type, self.tonnage)

        self.mdrive = drive
        
    def performance_by_volume(self, drive, drive_letter):
        """
        Handles checking whether a drive type is compatible and retrieves the relative jump/thrust numbers
        for a drive type
        :param drive: drive type
        :param drive_letter: letter of the drive 
        :return: None if incompatible
        """
        data = get_file_data("hull_performance.json")
        index = get_file_data("hull_performance_index.json")
        performance_list = data.get(drive_letter).get("jumps_per_hull_volume")

        # Get the nearest ton rounded down
        index = index.get(str(self.tonnage))

        # Error checking to see if drive type is incompatible with the hull size
        if index >= len(performance_list):
            return None

        value = performance_list[int(index)]

        # Error checking if the drive type is non-compatible with the hull size
        if value == 0:
            return None

        if drive == "mdrive":
            self.thrust = value
        if drive == "jdrive":
            self.jump = value

        return 1

    def get_lowest_drive(self):
        """
        Handles getting the lowest possible drive type for a given tonnage
        :return: letter of the drive type
        """
        data = get_file_data("hull_performance.json")
        index = get_file_data("hull_performance_index.json")
        idx = index.get(str(self.tonnage))

        for drive in data:
            jump_list = data.get(drive).get("jumps_per_hull_volume")

            # check invalid first, else return drive type
            if len(jump_list) <= idx:
                continue
            elif jump_list[idx] == 0:
                continue
            else:
                return drive

    def add_pplant(self, plant):
        """
        Adds a power plant to the spaceship
        :param plant: plant object
        """
        if self.tonnage == 0:
            return "Error: Tonnage not set before adding PPlant"

        self.pplant = plant
        self.fuel_two_weeks = plant.fuel_two_weeks
        return True

    def check_pplant_validity(self):
        """
        Checks whether the input pplant is valid based on the Drives
        """
        if self.pplant is not None:
            if None not in (self.mdrive, self.jdrive):
                max_drive = max(self.jdrive.drive_type, self.mdrive.drive_type)
                if self.pplant.type < max_drive:
                    return "Error: PPlant under max M/J-Drive. {} < {}".format(self.pplant.type, max(max_drive))
            elif self.jdrive is not None:
                if self.pplant.type < self.jdrive.drive_type:
                    return "Error: PPlant under J-Drive. {} < {}".format(self.pplant.type, self.jdrive.drive_type)
            elif self.mdrive is not None:
                if self.pplant.type < self.mdrive.drive_type:
                    return "Error: PPlant under M-Drive. {} < {}".format(self.pplant.type, self.mdrive.drive_type)
        return True

    def get_bridge_tonnage(self):
        """
        Handles calculating the cost of a main component bridge to the ship based on the hull size
        The bridge size is determined based upon the hull tonnage
        """
        bridge_tonnage = 0
        if self.tonnage < 300:
            bridge_tonnage = 10
        if 300 <= self.tonnage < 1100:
            bridge_tonnage = 20
        if 1100 <= self.tonnage < 2000:
            bridge_tonnage = 30
        if self.tonnage == 2000:
            bridge_tonnage = 40
        return bridge_tonnage

    def set_bridge(self):
        # Toggles bridge state
        self.bridge ^= True

    def add_computer(self, computer):
        """
        Handles adding/replacing a computer object in the ship
        :param computer: computer object to use
        """
        self.computer = computer

    def add_sensors(self, sensor):
        """
        Handles adding/replacing a sensors system within the system
        :param sensor: sensor object to use
        """
        self.sensors = sensor

    def add_bayweapon(self, weapon):
        """
        Handles adding a single bayweapon onto the ship
        :param weapon: weapon object to add
        """
        self.bays.append(weapon)

    def remove_bayweapon(self, weapon):
        """
        Handles removing a single bayweapon from a ship
        :param weapon: weapon object to remove
        """
        if weapon in self.bays:
            self.bays.remove(weapon)
        else:
            print("Error: bayweapon not attached to the ship.")

    def add_armour(self, armour):
        """
        Handles adding a piece of armour to the ship
        :param armour: armour object to add
        """
        self.armour_total += armour.protection
        self.armour.append(armour)

    def remove_armour(self, armour):
        """
        Handles removing a piece of armour from the ship
        :param armour: full armour string to be parse
        """
        if armour in self.armour:
            self.armour.remove(armour)
            self.armour_total -= armour.protection
        else:
            print("Error: armour piece not attached to the ship.")

    def edit_hull_config(self, config):
        """
        Updates hull config
        :param config: config object to use
        """
        self.hull_type = config

    def modify_hull_option(self, option):
        """
        Updates a hull option for a ship, adding it if it doesn't exist and removing it if it does
        :param option: Option object to use
        """
        for o in self.hull_options:
            if o.name == option.name:
                self.hull_options.remove(o)
                return
        self.hull_options.append(option)

    def modify_screen(self, screen):
        """
        Updates a screen for a ship, adding it if it doesn't exist, removing it if it does
        :param screen: Screen object to use
        """
        for s in self.screens:
            if screen.name == s.name:
                self.screens.remove(s)
                return
        self.screens.append(screen)

    def check_rating_ratio(self):
        # Calculates available software rating based on installed software and computer capabilities
        rating = 0
        for s in self.software:
            rating += s.rating

            # Check for Jump Control Spec giving one free rank
            if s.type == "Jump Control" and self.computer is not None and self.computer.bis:
                rating -= 5

        if self.computer is not None:
            available_rating = self.computer.rating - rating
        else:
            available_rating = 0 - rating

        return available_rating

    def modify_software(self, software):
        # Add/changes software
        for s in self.software:
            if s.type == software.type:
                self.software.remove(s)
                break

        self.software.append(software)

    def remove_software(self, software_name):
        # Removes software from ship
        for s in self.software:
            if s.type == software_name:
                self.software.remove(s)

    def modify_misc(self, misc):
        # Add/changes number of a misc item
        for m in self.misc:
            if m.name == misc.name:
                self.misc.remove(m)
                break

        self.misc.append(misc)

    def remove_misc(self, misc_name):
        # Removes misc from ship
        for m in self.misc:
            if m.name == misc_name:
                self.misc.remove(m)

    def modify_fuel_scoops(self):
        # Toggles fuel scoops state
        self.fuel_scoop ^= True

    def add_hardpoint(self, hp):
        # Adds a hardpoint to the ship
        self.hardpoints.append(hp)

    def remove_hardpoint(self, hp):
        # Removes a hardpoint from ship, if exists
        for h in self.hardpoints:
            if h is hp:
                self.hardpoints.remove(h)
