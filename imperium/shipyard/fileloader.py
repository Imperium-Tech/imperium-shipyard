"""
@file fileloader.py
@author qu-gg

Class that handles interacting with and saving a ship's state into a file for later use
"""
from imperium.classes.hardpoint import Hardpoint
from imperium.classes.software import Software
from imperium.classes.spacecraft import Spacecraft
from imperium.classes.turrets import Turret
from imperium.classes.misc import Misc
import json
import os


class FileLoader:
    def __init__(self):
        self.savepath = "models/"

    def save_model(self, outpath, spacecraft):
        """
        Handles the saving of a model by outputting the contents of the spacecraft into
        a formatted SRD file
        :param outpath: full path to the saved file
        :param spacecraft: spacecraft object to save
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
        else:
            template['computer']['model'] = "---"

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

        # Saving model to srd file
        with open(outpath, 'w') as f:
            json.dump(template, f)

    def load_model(self, path, window):
        """
        Handles loading in a model from a SRD file and setting both the backend and front end to the
        contents of the file
        :param path: full path to the file
        :param window: QMainWindow object to interact with
        """
        # Loading in the model template for ships
        with open(path, 'r') as f:
            model = json.load(f)

        # Wiping out the active turret box
        for i in reversed(range(0, window.turret_config_layout.count())):
            window.turret_config_layout.itemAt(i).widget().setParent(None)

        # Setting hull option flags to False initially
        window.reflec_check.setChecked(False)
        window.stealth_check.setChecked(False)
        window.seal_check.setChecked(False)
        window.fuel_scoop.setChecked(False)

        # Setting screen option flags to False initially
        window.meson_screen.setChecked(False)
        window.nuclear_damper.setChecked(False)

        # Adding software labels back to box
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../resources/hull_software.json")
        with open(path) as f:
            data = json.load(f)

        window.software_box.clear()
        window.software_box.addItem("---")
        for item in data.keys():
            window.software_box.addItem(item)

        # Adding misc labels back to box
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../resources/hull_misc.json")
        with open(path) as f:
            data = json.load(f)

        window.misc_dict = {}
        idx = 1
        window.misc_box.clear()
        window.misc_box.addItem(" ")
        for item in data.keys():
            window.misc_dict[item] = idx
            window.misc_box.addItem(item)
            idx += 1

        # Setting spacecraft to new template
        window.spacecraft = Spacecraft(100)

        # Setting stats
        window.tonnage_box.setCurrentText(str(model['stats']['tonnage']))
        window.edit_tonnage()

        window.fuel_line_edit.setText(str(model['stats']['fuel']))
        window.edit_fuel()

        window.discount.setText(str(round(100 * (1 - model['stats']['discount']))))
        window.edit_discount()

        # Setting drives
        window.jump_label.setText("-")
        window.thrust_label.setText("-")
        window.pplant_label.setText("-")

        if model['drives']['jdrive'] is not None:
            window.jump_line_edit.setText(model['drives']['jdrive'])
            window.edit_jdrive()

        if model['drives']['mdrive'] is not None:
            window.thrust_line_edit.setText(model['drives']['mdrive'])
            window.edit_mdrive()

        if model['drives']['pplant'] is not None:
            window.pplant_line_edit.setText(model['drives']['pplant'])
            window.edit_pplant()

        # Setting configs
        window.bridge_check.setChecked(model['config']['bridge'])
        window.check_bridge()

        options = model['config']['options']
        if options[0] is True:
            window.reflec_check.setChecked(True)

        if options[1] is True:
            window.seal_check.setChecked(True)

        if options[2] is True:
            window.stealth_check.setChecked(True)

        screens = model['config']['screens']
        if screens[0] is True:
            window.meson_screen.setChecked(True)

        if screens[1] is True:
            window.nuclear_damper.setChecked(True)

        window.hull_config_box.setCurrentText(model['config']['hull_type'])
        window.edit_hull_config()

        # Check for checked fuel scoops when standard config
        if model['config']['hull_type'] not in ['Distributed', 'Streamlined']:
            window.fuel_scoop.setChecked(model['config']['fuel_scoop'])

        window.sensors.setCurrentText(model['config']['sensors'])
        window.edit_sensors()

        # Redisplaying armour before adding rest
        window.edit_armor()
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
            window.software_box.setCurrentText(sname)
            window.software_box.removeItem(window.software_box.currentIndex())

        window.software_box.setCurrentIndex(0)
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
            if turret_dict is not None:
                turret = Turret(turret_dict['type'])
                turret.weapons = turret_dict['weapons']
                turret.missiles = turret_dict['missiles']
                turret.sandcaster_barrels = turret_dict['sandcaster_barrels']
                hp.add_turret(turret)

            window.spacecraft.add_hardpoint(hp)

        # Resetting HP total/avail
        window.total_hp.setText(str(window.spacecraft.num_hardpoints))
        window.avail_hp.setText(str(window.spacecraft.num_hardpoints - len(window.spacecraft.hardpoints)))

        # Setting active hardpoint to None, displaying new hardpoints
        window.active_hp_id = None
        window.display_hardpoints()

        # Updating stats at end
        window.update_stats()
