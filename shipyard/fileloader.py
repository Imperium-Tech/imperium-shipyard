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
            if option.name == "Reflec":
                template['config']['options'][0] = True
            elif option.name == "Self-Sealing":
                template['config']['options'][1] = True
            elif option.name == "Stealth":
                template['config']['options'][2] = True

        for screen in spacecraft.screens:
            if screen.name == "Meson Screen":
                template['config']['screens'][0] = True
            elif screen.name == "Nuclear Damper":
                template['config']['screens'][1] = True

        template['config']['fuel_scoop'] = spacecraft.fuel_scoop
        template['config']['hull_type'] = spacecraft.hull_type.type
        template['config']['sensors'] = spacecraft.sensors.name

        for armor in spacecraft.armour:
            template['config']['armour'].append(armor.type)

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

    def load_model(self, filename, window):
        print(filename, window)

        # Loading in the model template for ships
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "models/" + filename + ".srd")
        with open(path, 'r') as f:
            model = json.load(f)

        print(model)

        # Setting to new spacecraft
        window.spacecraft = Spacecraft(100)

        # Setting stats
        window.tonnage_box.setCurrentText(str(model['stats']['tonnage']))
        window.edit_tonnage()

        window.fuel_line_edit.setText(str(model['stats']['fuel']))
        window.edit_fuel()

        window.discount.setText(str(round(100 * (1 - model['stats']['discount']))))
        window.edit_discount()

        # Setting drives
        window.jump_line_edit.setText(model['drives']['jdrive'])
        window.edit_jdrive()

        window.thrust_line_edit.setText(model['drives']['mdrive'])
        window.edit_mdrive()

        window.pplant_line_edit.setText(model['drives']['pplant'])
        window.edit_pplant()

        # Setting configs
        window.bridge_check.setChecked(model['config']['bridge'])
        window.check_bridge()

        options = model['config']['options']
        window.reflec_check.setChecked(options[0])
        window.seal_check.setChecked(options[1])
        window.stealth_check.setChecked(options[2])

        screens = model['config']['screens']
        window.meson_screen.setChecked(screens[0])
        window.nuclear_damper.setChecked(screens[1])

        window.hull_config_box.setCurrentText(model['config']['hull_type'])
        window.edit_hull_config()

        # Check for checked fuel scoops when standard config
        if model['config']['hull_type'] not in ['Distributed', 'Streamlined']:
            window.fuel_scoop.setChecked(model['config']['fuel_scoop'])

        window.sensors.setCurrentText(model['config']['sensors'])
        window.edit_sensors()

        for armour in model['config']['armour']:
            window.armor_combo_box.setCurrentText(armour)
            window.edit_armor()

        # Editing computer/software
        window.computers.setCurrentText(model['computer']['model'])
        window.edit_computer()

        window.jump_control_spec.setChecked(model['computer']['jump_control_spec'])
        window.hardened_system.setChecked(model['computer']['hardened_system'])

        for sname, slevel in model['computer']['software']:
            window.spacecraft.modify_software(Software(sname, slevel))
        window.display_software()

        # Adding all misc items
        for mname, mnumber in model['misc']['misc']:
            window.spacecraft.modify_misc(Misc(mname, mnumber))
        window.display_misc_items()

        # Adding hardpoints and turrets
        for hardpoint in model['hardpoints']:
            # Making hp object
            hp = Hardpoint(hardpoint['id'])

            # Modifying its addons
            if hardpoint['popup']:
                hp.modify_addon('Pop-up Turret')
            if hardpoint['fixed']:
                hp.modify_addon('Fixed Mounting')

            # Making turret and adding it
            turret_dict = hardpoint['turret']
            turret = Turret(turret_dict['type'])
            turret.weapons = turret_dict['weapons']
            turret.missiles = turret_dict['missiles']
            turret.sandcaster_barrels = turret_dict['sandcaster_barrels']
            hp.add_turret(turret)

            window.spacecraft.add_hardpoint(hp)

        # Setting active hardpoint to None, displaying new hardpoints
        window.active_hp_id = None
        window.display_hardpoints()

        # Updating stats at end
        window.update_stats()
