"""
shipyard.py

Entrypoint for the imperium-shipyard program (https://github.com/Milkshak3s/imperium-shipyard)
"""
import data_generators as dg
from models.spacecraft import Spacecraft

new_spacecraft = Spacecraft(2001)

print(new_spacecraft.cost_total)