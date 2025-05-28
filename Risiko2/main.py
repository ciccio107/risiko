import json
import os
from gui import GUI


class Player:
    def __init__(self, name):
        self.name = name
        self.territories = []

    def add_territory(self, territory):
        self.territories.append(territory)

    def remove_territory(self, territory):
        if territory in self.territories:
            self.territories.remove(territory)

class Territory:
    def __init__(self, name, neighbors, owner=None, troops=1):
        self.name = name
        self.neighbors = neighbors  # lista di nomi territori confinanti
        self.owner = owner
        self.troops = troops

def load_territories(json_path, players):
    with open(json_path, "r") as f:
        data = json.load(f)

    territories = {}
    player_cycle = [players[0], players[1]]
    i = 0

    for territory_name, info in data.items():
        neighbors = info["neighbors"]
        owner = player_cycle[i % 2]
        i += 1

        territory = Territory(territory_name, neighbors, owner, troops=1)
        territories[territory_name] = territory

        owner.add_territory(territory)

    return territories

if __name__ == "__main__":
    gui = GUI()
    gui.run()
