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