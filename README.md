<img src="images/IS-banner.png" alt="Imperium Shipyard Banner"></img>

[![CircleCI](https://circleci.com/gh/Milkshak3s/imperium-shipyard.svg?style=svg)](https://circleci.com/gh/Milkshak3s/imperium-shipyard)
[![Coverage Status](https://coveralls.io/repos/github/Milkshak3s/imperium-shipyard/badge.svg?branch=master)](https://coveralls.io/github/Milkshak3s/imperium-shipyard?branch=master)  
Python ship designer for Mongoose Traveller SRD, 2nd Edition. Built using PyQT GUI and a JSON backend for data management
parsing. Utilizes a custom file format (.srd) in order to save, load, and share ships.

## Running:
There are two ways to run Imperium Shipyard, either through a cmd command or by using the executable provided. The CMD 
option is more for development work and testing features/tweaks.

For CMD (in root folder of imperium-shipyard): `python -m imperium.shipyard`

For EXE: simply double click the Imperium executable


## Custom Parts:
Imperium Shipyard allows for easily adding customized parts to various parts for the ship. This is done by parsing the JSON 
backend on runtime, so simply adding a new item to their respective JSON files in the resources folder will add the part to use.

#### Available custom parts include:
<ul>
    <li>Hull Config</li>
    <li>Sensors</li>
    <li>Armour</li>
    <li>Computer Models</li>
    <li>Software/Software Levels</li>
    <li>Any Misc Items</li>
    <li>Sensors</li>
    <li>Turret Models/Weapons</li>
</ul>

#### Instructions for adding:
For example, to add a new Sensor tier, you simply add a new JSON item into the respective "hull_sensors.json" file according to the
attributes of the others.

Adding an item to the JSON:

<img src="images/custom_sensor.PNG" alt="Image of JSON file"></img>

After rereunning the program, if done correctly, you'll see the new part in its combobox:

<img src="images/added_sensor.png" alt="Sensor in ComboBox"></img>

And there you go, a custom part to use in your ships!

<img src="images/custom_stats.PNG" alt="Picture of stats with custom sensor"></img>


## TO-DO:
There are still a number of features wanting to be implemented that aren't explicitly needed for the base functionality
of the program, but would be great additions to have.

These include:
<ul>
    <li><b> Shipyard Refactor</b>: the current blobs that are the shipyard.py/spacecraft.py would be nice to refactor into
    different sections based off of relatedness, like an "armory" for turrets, weapons, etc.</li>
    <li> <b>Starting Ship Templates</b>: after the file format, having the templates from the Core Rulebook ready to use would
    a nice starting point for newcomers.</li>
</ul>

Proposed Design Refactor:

<img src="images/imperium_design.png" alt="Picture of redesign"></img>
