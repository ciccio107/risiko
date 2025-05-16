from mappa import carica_mappa
from player import Player
from territory import Territory
from gui import avvia_gui  # importa la GUI

def mostra_mappa(territori):
    print("\n-- Mappa attuale --")
    for territorio in territori.values():
        print(territorio)

def mostra_confini(territori):
    print("\n-- Confini tra territori --")
    for territorio in territori.values():
        print(f"{territorio.name} confina con: {', '.join(territorio.neighbors)}")

if __name__ == "__main__":
    # Carica la mappa dal file JSON
    territori = carica_mappa("map.json")

    # Crea due giocatori
    player1 = Player("Giocatore 1")
    player2 = Player("Giocatore 2")
    players = [player1, player2]

    # Distribuisci territori e truppe ai giocatori
    Territory.distribuisci(territori, players, truppe_totali_per_giocatore=40)

    # Se vuoi puoi ancora vedere la mappa e i confini in console:
    mostra_mappa(territori)
    mostra_confini(territori)

    # Lancia la GUI per visualizzare la mappa graficamente
    avvia_gui(territori)
