import json
import os
from gui import GUI  # importa direttamente la classe GUI da gui.py

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

def main():
    player1 = Player("Giocatore 1")
    player2 = Player("Giocatore 2")

    json_path = os.path.join("assets", "map.json")
    territories = load_territories(json_path, [player1, player2])

    gui = GUI()  # crea istanza GUI correttamente
    gui.run()    # avvia la GUI (devi avere un metodo run() in GUI)

if __name__ == "__main__":
    main()
