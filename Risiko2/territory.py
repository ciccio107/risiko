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


def can_move_troops(from_territory, to_territory, player):
    return (
            from_territory.owner == player and
            to_territory.owner == player and
            to_territory.name in from_territory.neighbors and
            from_territory.troops > 1
    )


def move_troops(from_territory, to_territory, num_troops):
    if num_troops < 1 or from_territory.troops <= num_troops:
        return False
    from_territory.troops -= num_troops
    to_territory.troops += num_troops
    return True
    selected_from = None
    selected_to = None

    def handle_territory_click(territory, current_player):
        global selected_from, selected_to
        if selected_from is None:
            if territory.owner == current_player and territory.troops > 1:
                selected_from = territory
                print(f"Hai selezionato {territory.name} per spostare truppe.")
        else:
            selected_to = territory
            if selected_to == selected_from:
                print("Territorio selezionato due volte. Annullato.")
                selected_from = None
                selected_to = None
                return

            if can_move_troops(selected_from, selected_to, current_player):
                try:
                    num = int(input(f"Quante truppe vuoi spostare da {selected_from.name} a {selected_to.name}? "))
                    if move_troops(selected_from, selected_to, num):
                        print(f"{num} truppe spostate.")
                    else:
                        print("Numero di truppe non valido.")
                except ValueError:
                    print("Input non valido.")
            else:
                print("Spostamento non permesso.")
            selected_from = None
            selected_to = None

