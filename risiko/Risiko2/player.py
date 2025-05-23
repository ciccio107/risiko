class Player:
    def __init__(self, name):
        self.name = name
        self.territories = []

    def __str__(self):
        return self.name

    def add_territory(self, territory):
        self.territories.append(territory)

    def remove_territory(self, territory):
        self.territories.remove(territory)

    def get_total_troops(self):
        return sum(t.troops for t in self.territories)
