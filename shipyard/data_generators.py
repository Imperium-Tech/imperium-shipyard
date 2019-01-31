"""
data_generators.py

Some generators for the data stored in resources
"""
import json


def generate_hull_data():
    """
    Generates a data dict for Hulls
    """
    hull_data = dict()

    for i in range(1, 21):
        temp_key = None

        if i <= 9:
            temp_key = i
        else:
            temp_key = chr(56+i)

        hull_data[temp_key] = dict()
        hull_data[temp_key]['tonnage'] = i * 100

        if i == 1:
            hull_data[temp_key]['cost'] = 2
        elif i >= 2 and i <= 4:
            hull_data[temp_key]['cost'] = i * 4
        elif i >= 5 and i <= 8:
            hull_data[temp_key]['cost'] = (i - 3) * 16
        else:
            hull_data[temp_key]['cost'] = i * 10

    j = json.dumps(hull_data, indent=4)
    print(j)


def generate_jdrive_data():
    """
    Generates a data dict for J-Drives
    """
    jdrive_data = dict()

    for i in range(0, 24):
        j = i
        if j >= 8:
            j = j + 1
        if j >= 14:
            j = j + 1
        
        temp_key = chr(65+j)
        jdrive_data[temp_key] = dict()
        jdrive_data[temp_key]["tonnage"] = 10 + (5 * i)
        jdrive_data[temp_key]["cost"] = 10 * (i + 1)

    j = json.dumps(jdrive_data, indent=4)
    print(j)


def generate_mdrive_data():
    """
    Generates a data dict for M-Drives
    """
    mdrive_data = dict()

    for i in range(0, 24):
        j = i
        if j >= 8:
            j = j + 1
        if j >= 14:
            j = j + 1
        
        temp_key = chr(65+j)
        mdrive_data[temp_key] = dict()

        if i == 0:
            mdrive_data[temp_key]["tonnage"] = 2
        else:
            mdrive_data[temp_key]["tonnage"] = 1 + (2 * i)

        mdrive_data[temp_key]["cost"] = 4 * (i + 1)

    j = json.dumps(mdrive_data, indent=4)
    print(j)


def generate_pplant_data():
    """
    Generates a data dict for P-Plant
    """
    pplant_data = dict()

    for i in range(0, 24):
        j = i
        if j >= 8:
            j = j + 1
        if j >= 14:
            j = j + 1
        
        temp_key = chr(65+j)
        pplant_data[temp_key] = dict()
        pplant_data[temp_key]["tonnage"] = 4 + (3 * i)
        pplant_data[temp_key]["cost"] = 8 * (i + 1)
        pplant_data[temp_key]["fuel_two_weeks"] = 2 * (i + 1)

    j = json.dumps(pplant_data, indent=4)
    print(j)


def generate_performance_data():
    """
    Generates Performance by Hull Volume measaurements
    Have to manually input the values for each Hull type in list chunks
    """
    performance_data = dict()

    # Iterates through all characters
    for val in range(26):
        char = chr(65 + val)

        # Ignoring characters 'O' and 'I'
        if char != "O" and char != "I":
            performance_data[char] = dict()

            # Taking an input of numbers and converting to integers
            tonnage_list = input("Enter tonnage list for {} (-1 to quit): ".format(char))
            values = tonnage_list.split()
            for i in range(len(values)):
                values[i] = int(values[i])

            performance_data[char]["jumps_per_hull_volume"] = values

    p = json.dumps(performance_data, indent=4)
    print(p)


def generate_bridge_data():
    """
    Generates bridge data compared ship size to bridge size
    """
    bridge_data = dict()

    ship_size = ["200_tons", "300_to_1000_tons", "1100_to_2000_tons", "2000_plus_tons"]

    bridge_size = 10
    for ship in ship_size:
        bridge_data[ship] = dict()
        bridge_data[ship]["tonnage"] = bridge_size
        bridge_data[ship]["cost_per_ton"] = 0.005
        bridge_size += 10

    b = json.dumps(bridge_data, indent=4)
    print(b)


def generate_computer_data():
    """
    Generates computer data for the main component
    """
    computer_data = dict()

    rating = 5
    for i in range(7):
        model = "model_{}".format(i + 1)
        computer_data[model] = dict()

        if i == 0:
            computer_data[model]["tl"] = 7
        if i == 1:
            computer_data[model]["tl"] = 9
        if i > 1:
            computer_data[model]["tl"] = i + 9

        computer_data[model]["rating"] = rating
        rating += 5

        cost = float(input("Enter the cost in MCr. for Model {}: ".format(i + 1)))
        computer_data[model]["cost"] = cost

    c = json.dumps(computer_data, indent=4)
    print(c)


def generate_electronics_data():
    """
    Generates electronics data for the main component
    """
    electronics_data = dict()
    electronics_list = ["standard", "basic_civilian", "basic_military", "advanced", "very_advanced"]

    tech_level = 8
    for system in electronics_list:
        print("{}".format(system))
        electronics_data[system] = dict()
        electronics_data[system]["tl"] = tech_level
        tech_level += 1

        dice_modifier = int(input("Enter DM: "))
        electronics_data[system]["sensors_dm"] = dice_modifier

        equipment = input("Enter equipment: ")
        electronics_data[system]["equipment"] = equipment.split()

        tons = int(input("Enter tonnage: "))
        electronics_data[system]["tonnage"] = tons

        cost = float(input("Enter cost (in MCr.): "))
        electronics_data[system]["cost"] = cost

    e = json.dumps(electronics_data, indent=4)
    print(e)


def generate_vehicle_drone_data():
    """
    Generates vehicle and drone data for ship additions
    Have to manually add notes/desc. on each, as well as special modifiers on each.
        i.e. Repair Drones weighing .01 x tonnage of the ship
    """
    vehicle_drone_data = dict()
    while True:
        vehicle = input("Enter vehicle name (q to quit): ")
        if vehicle == "q":
            break
        tonnage = float(input("Enter tonnage: "))
        cost = float(input("Enter cost (in MCr.): "))
        vehicle_drone_data[vehicle] = dict()
        vehicle_drone_data[vehicle]["tonnage"] = tonnage
        vehicle_drone_data[vehicle]["cost"] = cost
        vehicle_drone_data[vehicle]["notes"] = list()

    v = json.dumps(vehicle_drone_data, indent=4)
    print(v)


def generate_living_data():
    """
    Generates living data for ship addons like Staterooms and Low Berth
    Have to manually enter notes
    """
    living_data = dict()
    while True:
        room = input("Enter room name (q to quit): ")
        if room == "q":
            break

        cost = float(input("Enter cost (in MCr.): "))
        tonnage = float(input("Enter tonnage: "))

        living_data[room] = dict()
        living_data[room]["cost"] = cost
        living_data[room]["tonnage"] = tonnage
        if room == "Luxuries":
            modifier = int(input("Enter Steward modifier: "))
            living_data[room]["steward_modifier"] = modifier
        else:
            max_occupants = int(input("Enter max occupants: "))
            living_data[room]["max_occupants"] = max_occupants
        living_data[room]["notes"] = list()

    l = json.dumps(living_data, indent=4)
    print(l)


def generate_turret_data():
    """
    Generates turret, addon, and weapon data
    Have to manually input notes data on addons
    """
    turret_data = dict()

    turret_data["models"] = dict()
    turret_data["addons"] = dict()
    turret_data["weapons"] = dict()

    while True:
        type = input("Does this belong to models or addons or weapons? (q to quit): ")
        if type == "q":
            break

        if type == "models" or type == "addons":
            parameters = (input("Enter Name, TL, Tonnage, Cost (in MCr.): ")).split()
            name = parameters[0]
            turret_data[type][name] = dict()
            turret_data[type][name]['tl'] = int(parameters[1])
            turret_data[type][name]['tonnage'] = float(parameters[2])
            turret_data[type][name]['cost'] = float(parameters[3])

            if type == "models":
                num_weapons = int(input("Enter # of weapons: "))
                turret_data[type][name]['num_weapons'] = num_weapons
            if type == "addons":
                turret_data[type][name]['notes'] = list()

        if type == "weapons":
            parameters = (input("Enter Name, TL, Opt. Range, Damage, Cost (in MCr.): ")).split()
            name = parameters[0]
            turret_data[type][name] = dict()
            turret_data[type][name]['tl'] = int(parameters[1])
            turret_data[type][name]['opt_range'] = parameters[2]
            turret_data[type][name]['damage'] = parameters[3]
            turret_data[type][name]['cost'] = float(parameters[4])
            turret_data[type][name]['notes'] = list()

    t = json.dumps(turret_data, indent=4)
    print(t)


def generate_bayweapon_data():
    """
    Generates data for the bay weapons on a ship
    Manually input values and can add more weapons to the weapon_list
    """
    bayweapon_data = dict()

    weapon_list = ["Missile Bank", "Particle Beam", "Fusion Gun", "Meson Gun"]
    for wep in weapon_list:
        print(wep)
        bayweapon_data[wep] = dict()
        bayweapon_data[wep]['tl'] = int(input("TL: "))
        bayweapon_data[wep]['range'] = input("Range: ")
        bayweapon_data[wep]['damage'] = input("Damage: ")
        bayweapon_data[wep]['cost'] = int(input("Cost: "))
        bayweapon_data[wep]['notes'] = list()

    b = json.dumps(bayweapon_data, indent=4)
    print(b)


def generate_screen_data():
    """
    Generates data for the screens on a ship
    Manually input values and can edit notes and add new screens
    """
    screen_data = dict()

    screen_list = ["Nuclear Damper", "Meson Screen"]
    for screen in screen_list:
        print(screen)
        screen_data[screen] = dict()
        screen_data[screen]['tl'] = int(input("TL: "))
        screen_data[screen]['tonnage'] = int(input("Tonnage: "))
        screen_data[screen]['cost'] = int(input("Cost (MCr.): "))
        screen_data[screen]['effect'] = list()

    s = json.dumps(screen_data, indent=4)
    print(s)


def generate_software_data():
    """
    Generates levels of software data in the ship software system
    Modify the (i * x) values in the for loop to customize scaling factors
    """
    software_data = dict()

    levels = int(input("How many levels for this program?: "))
    program = input("Name of program: ")
    tl = int(input("Starting TL: "))
    rating = int(input("Starting rating: "))
    cost = float(input("Starting cost: "))

    software_data[program] = dict()
    software_data[program]['effect'] = list()

    for i in range(levels):
        software_data[program][i + 1] = dict()
        software_data[program][i + 1]['tl'] = tl + (2 * i)
        software_data[program][i + 1]['rating'] = rating + (i * 10)
        software_data[program][i + 1]['cost'] = cost + (i * 5)

    s = json.dumps(software_data, indent=4)
    print(s)


def generate_fuel_addon_data():
    """
    Generates data for fuel addons on ships
    These are manually set values
    """
    fuel_addon_data = dict()

    fuel_addon_data["Fuel Scoop"] = dict()
    fuel_addon_data["Fuel Scoop"]['cost'] = 1
    fuel_addon_data["Fuel Scoop"]['tonnage'] = 0
    fuel_addon_data["Fuel Scoop"]['effect'] = list()

    fuel_addon_data["Fuel Processor"] = dict()
    fuel_addon_data["Fuel Processor"]['cost'] = .05
    fuel_addon_data["Fuel Processor"]['tonnage'] = 1
    fuel_addon_data["Fuel Processor"]['fuel_refinement_rate'] = 20
    fuel_addon_data["Fuel Processor"]['effect'] = list()

    f = json.dumps(fuel_addon_data, indent=4)
    print(f)


generate_fuel_addon_data()

