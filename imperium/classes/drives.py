"""
drives.py

Contains classes for the M & J drives
"""
from imperium.classes.json_reader import get_file_data


class Drive:
    """
    A parent class for all drive types
    """
    def __init__(self, drive_type):
        self.drive_type = None  # the drive designation (A, F, H, etc.)
        self.tonnage    = 0     # the size of the drive in tons
        self.cost       = 0     # the cost of the drive

        # set drive type from init
        self.drive_type = drive_type


class JDrive(Drive):
    """
    The J-Drive, or Jump Drive, in a Spaceship
    
    :param drive_type: The type of J-Drive, by letter
    """
    def __init__(self, drive_type):
        Drive.__init__(self, drive_type)

        # grab additional info from json
        data = get_file_data("jdrive_data.json")
        drive_item = data.get(drive_type)

        # set determined object state
        self.tonnage = drive_item.get("tonnage")
        self.cost = drive_item.get("cost")


class MDrive(Drive):
    """
    The M-Drive, or Maneuver Drive, in a Spaceship
    
    :param drive_type: The type of M-Drive, by letter
    """
    def __init__(self, drive_type):
        Drive.__init__(self, drive_type)

        # grab additional info from json
        data = get_file_data("mdrive_data.json")
        drive_item = data.get(drive_type)

        # set determined object state
        self.tonnage = drive_item.get("tonnage")
        self.cost = drive_item.get("cost")
