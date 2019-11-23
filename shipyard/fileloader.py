"""
@file fileloader.py
@author qu-gg

Class that handles interacting with and saving a ship's state into a file for later use
"""
from imperium.models.armour import Armour
from imperium.models.computer import Computer
from imperium.models.drives import JDrive, MDrive
from imperium.models.hardpoint import Hardpoint
from imperium.models.pplant import PPlant
from imperium.models.software import Software
from imperium.models.spacecraft import Spacecraft
from imperium.models.option import Option
from imperium.models.misc import Misc
import json
import os

from imperium.models.turrets import Turret


class FileLoader:
    def __init__(self):
        self.savepath = "models/"

    def save_model(self, filename, spacecraft):
        """

        :param filename:
        :param spacecraft:
        :return:
        """

        # Loading in the model template for ships
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "model_template.json")
        with open(path, 'r') as f:
            template = json.load(f)

        # Putting into stats
        template['stats']['tonnage'] = spacecraft.tonnage
        template['stats']['cost'] = round(spacecraft.get_total_cost(), 3)
        template['stats']['cargo'] = spacecraft.get_remaining_cargo()
        template['stats']['fuel'] = spacecraft.fuel_max
        template['stats']['discount'] = spacecraft.discount

        # Adding drives
        if spacecraft.jdrive is not None:
            template['drives']['jdrive'] = spacecraft.jdrive.drive_type
        if spacecraft.mdrive is not None:
            template['drives']['mdrive'] = spacecraft.mdrive.drive_type
        if spacecraft.pplant is not None:
            template['drives']['pplant'] = spacecraft.pplant.type

        # Adding config options
        template['config']['bridge'] = spacecraft.bridge

        for option in spacecraft.hull_options:
            template['config']['options'].append(option.name)

        template['config']['fuel_scoop'] = spacecraft.fuel_scoop
        template['config']['hull_type'] = spacecraft.hull_type.type
        template['config']['sensors'] = spacecraft.sensors.name

        for armor in spacecraft.armour:
            template['config']['armor'].append(armor.type)

        # Adding computer and software
        if spacecraft.computer is not None:
            template['computer']['model'] = spacecraft.computer.model
            template['computer']['jump_control_spec'] = spacecraft.computer.bis
            template['computer']['hardened_system'] = spacecraft.computer.fib

        for software in spacecraft.software:
            template['computer']['software'].append((software.type, software.level))

        # Adding in all misc objects
        for misc in spacecraft.misc:
            template['misc']['misc'].append((misc.name, misc.num))

        # Adding in hardpoints
        for hardpoint in spacecraft.hardpoints:
            hp = {
                "id": hardpoint.id,
                "popup": hardpoint.popup,
                "fixed": hardpoint.fixed,
                "turret": None
            }
            if hardpoint.turret is not None:
                hp["turret"] = {
                    "type": hardpoint.turret.name,
                    "weapons": hardpoint.turret.weapons,
                    "missiles": hardpoint.turret.missiles,
                    "sandcaster_barrels": hardpoint.turret.sandcaster_barrels
                }
            template['hardpoints'].append(hp)

        print(template)

        # Saving model to srd file
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "models/" + filename + ".srd")
        with open(path , 'w') as f:
            json.dump(template, f)


if __name__ == '__main__':
    spacecraft = Spacecraft(100)
    spacecraft.add_jdrive(JDrive("A"))
    spacecraft.add_mdrive(MDrive("A"))
    spacecraft.add_pplant(PPlant("A"))
    spacecraft.modify_hull_option(Option("Stealth"))
    spacecraft.add_armour(Armour("Crystaliron"))
    spacecraft.add_computer(Computer("Model 4"))
    spacecraft.modify_software(Software("Jump Control", 3))
    spacecraft.modify_misc(Misc("Staterooms", 5))

    hp = Hardpoint("XSDFSB")
    hp.add_turret(Turret("Single Turret"))
    spacecraft.add_hardpoint(hp)


    fileloader = FileLoader()
    fileloader.save_model("testmodel", spacecraft)
