"""
spacecraft.py

Houses the spacecraft class
"""
from imperium.models.config import Config
from imperium.models.json_reader import get_file_data


class Spacecraft:
    """
    The Spacecraft, primary class for organizing spaceship data

    :param hull_tonnage: the size of the hull, in tons
    """
    def __init__(self, hull_tonnage):
        self.tonnage            = 0 # total tonnage of ship
        self.hull_hp            = 0 # calculated as 1 per 50 tonnage
        self.structure_hp       = 0 # calculated as 1 per 50 tonnage
        self.jump               = 0 # max number of tiles covered in a single jump
        self.thrust             = 0 # max number of G accelerations available
        self.fuel_max           = 0 # amount of fuel tank
        self.fuel_jump          = 0 # amount of fuel required for a jump
        self.fuel_two_weeks     = 0 # amount of fuel required for 2 weeks of operation
        self.armour_total       = 0 # total armour pointage
        self.hull_designation   = None   # A, B, C, etc.
        self.hull_type          = None   # steamlined, distributed, standard, etc.
        self.bridge             = False  # whether a bridge is installed
        self.jdrive             = None   # jdrive object
        self.mdrive             = None   # mdrive object
        self.pplant             = None   # pplant object
        self.armour             = list() # list of armour objects
        self.sensors            = None   # sensor object
        self.turrets            = list() # list of turret objects
        self.bays               = list() # list of bay objects
        self.screens            = list() # list of screen objects
        self.computer           = None   # computer object
        self.software           = list() # list of installed software
        self.drones             = list() # list of drone objects
        self.vehicles           = list() # list of vehicle objects
        self.additional_mods    = list() # list of strings describing misc features

        # set the tonnage to that given at init
        if hull_tonnage > 2000:
            hull_tonnage = 2000

        self.tonnage = hull_tonnage

        # set hp based on tonnage
        self.hull_hp = self.tonnage // 50
        self.structure_hp = self.tonnage // 50

        # pull hull cost from json, set that
        data = get_file_data("hull_data.json")

        for key in data.keys():
            # iterate through hull sizes for 
            item_tonnage = data.get(key).get("tonnage")
            if self.tonnage <= item_tonnage and (item_tonnage - self.tonnage) < 100:
                self.hull_designation = key

        # set hull type to standard
        self.hull_type = Config("Standard")

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

        # Drives
        if self.jdrive is not None:
            cost_total += self.jdrive.cost
        if self.mdrive is not None:
            cost_total += self.mdrive.cost
        if self.pplant is not None:
            cost_total += self.pplant.cost

        # Armour
        for armour_item in self.armour:
            cost = armour_item.cost_by_hull_percentage
            cost_total += int(self.tonnage * cost)

        # Sensors
        if self.sensors is not None:
            cost_total += self.sensors.cost

        # Turrets / Bayweapons
        for turret in self.turrets:
            cost_total += turret.cost
        for bayweapon in self.bays:
            cost_total += bayweapon.cost

        # Screens / Computer / Software
        for screen in self.screens:
            cost_total += screen.cost
        if self.computer is not None:
            cost_total += self.computer.cost
        for software in self.software:
            cost_total += software.cost

        # Drones / Vehicles
        for drone in self.drones:
            cost_total += drone.cost
        for vehicle in self.vehicles:
            cost_total += vehicle.cost
        for misc in self.additional_mods:
            cost_total += misc.cost

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
        for turret in self.turrets:
            cargo -= turret.tonnage
        for bayweapon in self.bays:
            cargo -= bayweapon.tonnage
        for screen in self.screens:
            cargo -= screen.tonnage

        # Drones / Vehicles / Misc
        for drone in self.drones:
            if drone.name == "Repair Drone":
                cargo -= drone.tonnage * self.tonnage
            else:
                cargo -= drone.tonnage
        for vehicle in self.vehicles:
            cargo -= vehicle.tonnage
        for misc in self.additional_mods:
            cargo -= misc.tonnage

        return cargo

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
        if self.performance_by_volume("jdrive", drive.drive_type) is not None:
            self.jdrive = drive
            return True
        else:
            return "Error: non-compatible drive to tonnage value - Drive {} to {}".format(drive.drive_type, self.tonnage)

    def add_mdrive(self, drive):
        """
        Adds a maneuver drive to the spaceship
        :param drive_type: The drive designation letter
        """
        if self.tonnage == 0:
            return "Error: Tonnage not set before adding m-drive."

        # Error checking to see if new drive type is incompatible
        if self.performance_by_volume("mdrive", drive.drive_type) is not None:
            self.mdrive = drive
            return True
        else:
            return "Error: non-compatible drive to tonnage value - Drive {} to {}".format(drive.drive_type, self.tonnage)
        
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

    def add_pplant(self, plant):
        """
        Adds a power plant to the spaceship
        # Todo - add error checking with m/j-drive
        :param plant_type: The plant designation letter
        """
        # assign object to ship, update cost & tonnage
        self.pplant = plant
        self.fuel_two_weeks = plant.fuel_two_weeks

    def add_turret(self, turret):
        """
        Adds a single turret to the spaceship
        :param turret: Turret object to append
        """
        self.turrets.append(turret)

    def remove_turret(self, turret_index):
        """
        Removes a single turret from the spaceship
        :param turret_index: Index of the turret to remove
        """
        if len(self.turrets) != (turret_index + 1):
            return

        turret = self.turrets[turret_index]
        self.turrets.remove(turret)

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

    def add_misc(self, misc):
        """
        Handles adding a single misc addon to the ship and updating tonnage
        Repair Drone and Escape Pods have special calculations for tonnage and is scaled accordingly
        """
        drones = ["Repair Drone", "Mining Drone", "Probe Drone"]
        vehicles = ["ATV", "Air/Raft", "Life Boat/Launch", "Ship's Boat", "Pinnace", "Cutter", "Shuttle"]

        if misc.name in drones:
            self.drones.append(misc)
        elif misc.name in vehicles:
            self.vehicles.append(misc)
        else:
            if misc.name == "Escape Pods" and self.get_staterooms() < 0:
                return "Error: no staterooms exist on this ship - escape pods cannot be added."
            self.additional_mods.append(misc)

    def remove_misc(self, misc):
        """
        Handles removing a single misc addon from the ship, adjusting tonnage
        Repair Drone and Escape Pods have special calculations for tonnage and is scaled accordingly
        """
        drones = ["Repair Drone", "Mining Drone", "Probe Drone"]
        vehicles = ["ATV", "Air/Raft", "Life Boat/Launch", "Ship's Boat", "Pinnace", "Cutter", "Shuttle"]

        if misc.name in drones:
            self.drones.remove(misc)
        elif misc.name in vehicles:
            self.vehicles.remove(misc)
        else:
            self.additional_mods.remove(misc)

    def get_staterooms(self):
        """
        Counts the number of staterooms present in the additional mods
        :return: number of staterooms
        """
        num_staterooms = 0
        for mod in self.additional_mods:
            if mod.name == "Stateroom":
                num_staterooms += 1
        return num_staterooms

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

    def add_screen(self, screen):
        """
        Handles adding a screen object to a ship
        Checks whether the module has already been added previously
        :param screen: screen object to add
        """
        for s in self.screens:
            if s.name == screen.name:
                return "Error: screen module already installed on ship."

        self.screens.append(screen)

    def remove_screen(self, screen):
        """
        Handles removing a screen object from the ship
        :param screen: screen object to remove
        """
        for s in self.screens:
            if s.name == screen.name:
                self.screens.remove(s)
                
    def add_software(self, software):
        """
        Handles adding/altering a piece of software on a ship. Contains error checking for
        computer rating limitations
        :param software: software to add
        """
        # Calculating the current total software rating
        current_rating = 0
        for s in self.software:
            current_rating += s.rating

        # Represents the combined rating between the current rating and software rating
        combined_rating = software.rating + current_rating

        # Checking whether software is already installed and adjusting combined_rating cost
        installed = False
        installed_s = None
        for s in self.software:
            if s.type == software.type:
                installed_s = s
                difference = software.rating - s.rating
                combined_rating = current_rating + difference
                installed = True
                break

        # Checking whether the new software exceeds the max computer rating
        if combined_rating > self.computer.rating:
            print("Error: cannot add software, exceeds computer rating limit - {}/{}".format(
                combined_rating, self.computer.rating
            ))
            return

        if installed:
            self.software.remove(installed_s)

        self.software.append(software)

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

