"""
spacecraft.py

Houses the spacecraft class
"""
from shipyard.models.json_reader import get_file_data
from shipyard.models.drives import JDrive
from shipyard.models.drives import MDrive
from shipyard.models.pplant import PPlant
from shipyard.models.turrets import Turret


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
        self.sensors            = list() # list of sensor objects
        self.turrets            = list() # list of turret objects
        self.bays               = list() # list of bay objects
        self.screens            = list() # list of screen objects
        self.computer           = list() # list of computer objects
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

    def add_jdrive(self, drive_type):
        """
        Adds a jump drive to the spaceship

        :param drive_type: The drive designation letter
        """
        # create new jdrive object
        new_jdrive = JDrive(drive_type)

        # if drive already in place, replace stats
        if self.jdrive is not None:
            self.cost_total = self.cost_total - self.jdrive.cost
            self.cargo = self.cargo + self.jdrive.tonnage

        # assign object to ship, update cost & tonnage
        self.jdrive = new_jdrive
        self.cost_total = self.cost_total + new_jdrive.cost
        self.cargo = self.cargo - new_jdrive.tonnage
        self.performance_by_volume("jdrive", drive_type)

    def add_mdrive(self, drive_type):
        """
        Adds a maneuver drive to the spaceship

        :param drive_type: The drive designation letter
        """
        # create new mdrive object
        new_mdrive = MDrive(drive_type)

        # if drive already in place, replace stats
        if self.mdrive is not None:
            self.cost_total = self.cost_total - self.mdrive.cost
            self.cargo = self.cargo + self.mdrive.tonnage

        # assign object to ship, update cost & tonnage
        self.mdrive = new_mdrive
        self.cost_total = self.cost_total + new_mdrive.cost
        self.cargo = self.cargo - new_mdrive.tonnage
        self.performance_by_volume("mdrive", drive_type)

    def performance_by_volume(self, drive, drive_letter):
        data = get_file_data("hull_performance.json")
        index = get_file_data("hull_performance_index.json")
        performance_list = data.get(drive_letter).get("jumps_per_hull_volume")

        # Get the nearest ton rounded down
        ton = round(self.tonnage)
        index = index.get(str(ton))
        value = performance_list[index]

        # Error checking if the drive type is non-compatible with the hull size
        if value == 0:
            print("Error: non-compatible drive to tonnage value - {} to {}".format(drive, self.tonnage))
            return None

        if drive == "mdrive":
            self.thrust = value
        if drive == "jdrive":
            self.jump = value

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




