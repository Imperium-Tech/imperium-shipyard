"""
spacecraft.py

Houses the spacecraft class
"""
from imperium.models.json_reader import get_file_data
from imperium.models.drives import JDrive
from imperium.models.drives import MDrive
from imperium.models.pplant import PPlant


class Spacecraft:
    """
    The Spacecraft, primary class for organizing spaceship data

    :param hull_tonnage: the size of the hull, in tons
    """
    def __init__(self, hull_tonnage):
        self.tonnage            = 0 # total tonnage of ship
        self.hull_hp            = 0 # calculated as 1 per 50 tonnage
        self.structure_hp       = 0 # calculated as 1 per 50 tonnage
        self.cargo              = 0 # amount of cargo space in tons (total tonnage - fuel - other modules)
        self.jump               = 0 # max number of tiles covered in a single jump
        self.thrust             = 0 # max number of G accelerations available
        self.fuel_max           = 0 # amount of fuel tank
        self.fuel_jump          = 0 # amount of fuel required for a jump
        self.fuel_two_weeks     = 0 # amount of fuel required for 2 weeks of operation
        self.cost_hull          = 0 # cost of the hull alone
        self.cost_total         = 0 # current cost, updated on each edit
        self.hull_designation   = None   # A, B, C, etc.
        self.hull_type          = None   # steamlined, distributed, standard, etc.
        self.jdrive             = None   # jdrive object
        self.mdrive             = None   # mdrive object
        self.pplant             = None   # pplant object
        self.armour             = list() # list of armor objects
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

        # set cargo to maximum possible at first
        self.cargo = hull_tonnage

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
                self.cost_hull = data.get(key).get("cost")

        if self.cost_hull == 0:
            # picked an invalid hull size
            return None
        
        # set the total cost to hull cost
        self.cost_total = self.cost_hull

    def set_tonnage(self, new_tonnage):
        """
        Sets the tonnage of an existing Spacecraft
        :param new_tonnage: The tonnage to update to
        """
        tonnage_cost_data = get_file_data("hull_data.json")
        new_cost = 0
        for key in tonnage_cost_data:
            current = tonnage_cost_data.get(key)
            if current.get('tonnage') == self.tonnage:
                self.cost_total -= current.get("cost")
            if current.get('tonnage') == int(new_tonnage):
                new_cost = current.get("cost")

        self.cargo = self.cargo + (new_tonnage - self.tonnage)
        self.tonnage = new_tonnage
        self.cost_total += new_cost

    def set_fuel(self, new_fuel):
        """
        Sets the max fuel of an existing Spacecraft
        :param new_fuel: The fuel to update to
        """
        self.cargo = self.cargo - new_fuel
        self.fuel_max = new_fuel

    def add_jdrive(self, drive_type):
        """
        Adds a jump drive to the spaceship
        :param drive_type: The drive designation letter
        """
        # create new jdrive object
        new_jdrive = JDrive(drive_type)

        # Error checking to see if new drive type is incompatible
        if self.performance_by_volume("jdrive", drive_type) is not None:
            # if drive already in place, replace stats
            if self.jdrive is not None:
                self.cost_total = self.cost_total - self.jdrive.cost
                self.cargo = self.cargo + self.jdrive.tonnage

            # assign object to ship, update cost & tonnage
            self.jdrive = new_jdrive
            self.cost_total = self.cost_total + new_jdrive.cost
            self.cargo = self.cargo - new_jdrive.tonnage
        

    def add_mdrive(self, drive_type):
        """
        Adds a maneuver drive to the spaceship
        :param drive_type: The drive designation letter
        """
        # create new mdrive object
        new_mdrive = MDrive(drive_type)

        # Error checking to see if new drive type is incompatible
        if self.performance_by_volume("mdrive", drive_type) is not None:
            # if drive already in place, replace stats
            if self.mdrive is not None:
                self.cost_total = self.cost_total - self.mdrive.cost
                self.cargo = self.cargo + self.mdrive.tonnage

            # assign object to ship, update cost & tonnage
            self.mdrive = new_mdrive
            self.cost_total = self.cost_total + new_mdrive.cost
            self.cargo = self.cargo - new_mdrive.tonnage
        

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
            print("Error: non-compatible drive to tonnage value - Drive {} to {}".format(drive_letter, self.tonnage))
            return None

        value = performance_list[int(index)]

        # Error checking if the drive type is non-compatible with the hull size
        if value == 0:
            print("Error: non-compatible drive to tonnage value - Drive {} to {}".format(drive_letter, self.tonnage))
            return None

        if drive == "mdrive":
            self.thrust = value
        if drive == "jdrive":
            self.jump = value

        return 1

    def add_pplant(self, plant_type):
        """
        Adds a power plant to the spaceship
        :param plant_type: The plant designation letter
        """
        # create new pplant object
        new_pplant = PPlant(plant_type)

        # if plant already in place, replace stats
        if self.pplant is not None:
            self.cost_total = self.cost_total - self.pplant.cost
            self.cargo = self.cargo + self.pplant.tonnage

        # assign object to ship, update cost & tonnage
        self.pplant = new_pplant
        self.cost_total = self.cost_total + new_pplant.cost
        self.cargo = self.cargo - new_pplant.tonnage
        self.fuel_two_weeks = new_pplant.fuel_two_weeks

    def add_turret(self, turret):
        """
        Adds a single turret to the spaceship and adds costs to
        :param turret: Turret object to append
        """
        self.turrets.append(turret)
        self.cargo -= turret.tonnage
        self.cost_total += turret.cost

    def remove_turret(self, turret_index):
        """
        Removes a single turret from the spaceship and decrements costs
        :param turret_index: Index of the turret to remove
        """
        if len(self.turrets) != (turret_index + 1):
            return

        turret = self.turrets[turret_index]
        self.turrets.remove(turret)
        self.cargo += turret.tonnage
        self.cost_total -= turret.cost

    def add_bridge(self):
        """
        Handles adding a main component bridge to the ship based on the hull size
        The bridge size is determined based upon the hull tonnage
        """
        if self.tonnage < 300:
            self.cargo -= 10
        if 300 <= self.tonnage < 1100:
            self.cargo -= 20
        if 1100 <= self.tonnage < 2000:
            self.cargo -= 40
        if self.tonnage == 2000:
            self.cargo -= 60

        self.cost_total += 0.5 * round(self.tonnage // 100)

    def get_armor_rating(self):
        """
        Gets the total armor rating for the ship

        :returns: An int representing the total armor
        """
        total_rating = 0

        for armour_item in self.armour:
            protection = armour_item.get('protection')
            if protection is not None:
                total_rating = total_rating + protection

        return total_rating
        
    def add_misc(self, misc):
        """
        Handles adding a single misc addon to the ship and updating tonnage/cost
        Repair Drone and Escape Pods have special calculations for tonnage and is scaled accordingly
        """
        self.additional_mods.append(misc)
        self.cost_total += misc.cost

        tonnage = misc.tonnage
        if misc.name == "Repair Drone":
            tonnage = misc.tonnage * self.tonnage
        if misc.name == "Escape Pods":
            if self.get_staterooms() > 0:
                tonnage = misc.tonnage * self.get_staterooms()
            else:
                print("Error: no staterooms exist on this ship - escape pods cannot be added.")

        self.cargo -= tonnage

    def remove_misc(self, misc):
        """
        Handles removing a single misc addon from the ship, adjusting tonnage/cost
        Repair Drone and Escape Pods have special calculations for tonnage and is scaled accordingly
        """
        self.additional_mods.append(misc)
        self.cost_total -= misc.cost

        tonnage = misc.tonnage
        if misc.name == "Repair Drone":
            tonnage = misc.tonnage * self.tonnage
        if misc.name == "Escape Pods":
            tonnage = misc.tonnage * self.get_staterooms()

        self.cargo += tonnage

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
        Handles adding/replacing a computer object in the ship, adjusting cost as needed
        :param computer: computer object to use
        """
        if self.computer is not None:
            self.cost_total -= self.computer.cost

        self.computer = computer
        self.cost_total += computer.cost
        
    def add_sensors(self, sensor):
        """
        Handles adding/replacing a sensors system within the system, adjusting cost/tonnage
        :param sensor: sensor object to use
        """
        if self.sensors is not None:
            self.cargo += self.sensors.tonnage
            self.cost_total -= self.sensors.cost

        self.sensors = sensor
        self.cargo -= sensor.tonnage
        self.cost_total += sensor.cost

    def add_screen(self, screen):
        """
        Handles adding a screen object to a ship, adjusting cost/tonnage
        Checks whether the module has already been added previously
        :param screen: screen object to add
        """
        for s in self.screens:
            if s.name == screen.name:
                print("Error: screen module already installed on ship.")
                return

        self.screens.append(screen)
        self.cost_total += screen.cost
        self.cargo -= screen.tonnage

    def remove_screen(self, screen):
        """
        Handles removing a screen object from the ship
        :param screen: screen object to remove
        """
        for s in self.screens:
            if s.name == screen.name:
                self.cost_total -= s.cost
                self.cargo += s.tonnage
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
            self.cost_total -= installed_s.cost

        self.software.append(software)
        self.cost_total += software.cost
