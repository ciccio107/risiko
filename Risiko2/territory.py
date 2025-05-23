import random

class Territory:
    def __init__(self, name, neighbors, continent):
        self.name = name
        self.neighbors = neighbors
        self.continent = continent
        self.owner = None
        self.troops = 0

    def __str__(self):
        owner = self.owner.name if self.owner else "Nessuno"
        return f"{self.name} ({self.continent}) - Proprietario: {owner} - Truppe: {self.troops}"

    @classmethod
    def distribuisci(cls, territori: dict, players: list, truppe_totali_per_giocatore: int = 40):
        lista_territori = list(territori.values())
        random.shuffle(lista_territori)

        for i, territorio in enumerate(lista_territori):
            player = players[i % len(players)]
            territorio.owner = player
            territorio.troops = 1
            player.add_territory(territorio)

        for player in players:
            truppe_da_distribuire = truppe_totali_per_giocatore - len(player.territories)
            while truppe_da_distribuire > 0:
                territorio = random.choice(player.territories)
                territorio.troops += 1
                truppe_da_distribuire -= 1

