<img src="images/IS-banner.png" alt="Imperium Shipyard Banner"></img>

[![CircleCI](https://circleci.com/gh/Imperium-Tech/imperium-shipyard.svg?style=svg)](https://circleci.com/gh/Imperium-Tech/imperium-shipyard)

[![Coverage Status](https://coveralls.io/repos/github/Milkshak3s/imperium-shipyard/badge.svg?branch=master)](https://coveralls.io/github/Milkshak3s/imperium-shipyard?branch=master)  
Python ship designer for Mongoose Traveller SRD, 1st Edition. Built using PyQT GUI and a JSON backend for data management/parsing. Utilizes a custom file format (.srd) in order to save, load, and share ships. 


## Running:
There are two ways to run Imperium Shipyard, either through a cmd command by pulling the repo or by using the executable provided from our release page. The CMD option is more for development work and testing new features/tweaks, as well for those on MacOS/Linux.

For CMD (in root folder of imperium-shipyard): `python shipbuilder.py`

For EXE: simply double click the Imperium executable within the root of ImperiumShipyard/

## Folder Layout:
```
  ImperiumShipyard/
  │
  ├── ImperiumShipyard.exe
  |
  ├── imperium/
  │   ├── resources/ - Holds the transcribed table values from the rulebook
  │   └── shipyard/  - Repository for holding .srd files
  ```

## Default Ships:
Included standard in Imperium Shipyard is a representation of every ship available in the Core Rulebooks, from the Laboratory Ship to the Corsair. The costs of these ships equally match the raw added totals in all cases. 

These ships can be loaded in via the file bar and are found within ImperiumShipyard/imperium/shipyard/models/default.
For creating custom ships by hand (outside of the program), the default.srd or model_template.json files can be used as references.

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

These could be good issues to tackle (some far more work than others) for those looking to contribute! :)

These include:
<ul>
    <li><b> Shipyard Refactor</b>: the current blobs that are the shipyard.py/spacecraft.py would be nice to refactor into
    different sections based off of relatedness, like an "armory" for turrets, weapons, etc.</li>
    <li><b> UI Rework</b>: while most of the sections are clean, the stat tracking for hardpoints can be cleaned up and condensed. One idea is to condense it into one column that has drop-down lists for each piece and can scroll like the other columns.</li>
    <li><b> Armor UI</b>: presently, you need to click on the added armor to remove it. This is inconsistent with the other features having "remove" buttons, so bringing this in line would help consistency. It appears to be an alignment nightmare, though.</li>
  <li><b> GUI Sizing</b>: at the moment, window size values are mostly hardcoded rather than dynamically fitted. It functions well at 1080p+ resolution on a Windows machine, but it might look off on other OSs or resolutions.</li>
  <li><b> Mouseover Equipment</b>: There are a lot of fields that don't affect values in the calculator but are present in our backend. Having a way to visualize attached equipment (perhaps with a mouseover menu on specific items?) would be a convenient feature to have.</li>
  <li><b> Error Logger</b>: while the rules in the books are enforced on what is allowed under which circumstances, having an error logger on why specific things are wrong would be helpful to newer players.</li>
</ul>

Proposed Design Refactor:

<img src="images/imperium_design.png" alt="Picture of redesign"></img>

## Issues and Contributions
Please feel free to put up any issues that are found or enhancements that would improve this work. As well, please feel welcome to put up PRs for any improvements that you can do!

## Credit
The ship design in our icon comes from Greer Mosher, available here: https://thenounproject.com/term/spaceship/269595/

This icon is available as a sample icon on Adobe Spark's Logo Maker under the CC License.
