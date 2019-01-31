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


def generate_powerplant_data():
    """
    Generates data regarding Ship Powerplant fuel usage
    """
    powerplant_data = dict()

    tons = 2
    # Iterates through all characters
    for val in range(26):
        char = chr(65 + val)

        # Ignoring characters 'O' and 'I'
        if char != "O" and char != "I":
            powerplant_data[char] = dict()
            powerplant_data[char]["tons_per_two_weeks"] = tons
            tons += 2

    p = json.dumps(powerplant_data, indent=4)
    print(p)


def generate_bridge_data():
    """
    Generates bridge data compared ship size to bridge size
    """
    bridge_data = dict()

    bridge_data["200_tons"] = 10
    bridge_data["300_to_1000_tons"] = 20
    bridge_data["1100_to_2000_tons"] = 30
    bridge_data["2000_plus_tons"] = 40

    b = json.dumps(bridge_data, indent=4)
    print(b)
