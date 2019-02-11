"""
shipyard.py

Entrypoint for the imperium-shipyard program (https://github.com/Milkshak3s/imperium-shipyard)
"""
import data_generators as dg
from models.spacecraft import Spacecraft


def main():
    new_spacecraft = Spacecraft(2000)

    print(new_spacecraft.cost_total)


if __name__ == "__main__":
    main()
