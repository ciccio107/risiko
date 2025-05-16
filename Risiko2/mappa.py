import json
from territory import Territory

def carica_mappa(file_json):
    with open(file_json, "r") as f:
        dati = json.load(f)

    territori = {}
    for nome, info in dati.items():
        territorio = Territory(
            name=nome,
            neighbors=info["neighbors"],
            continent=info["continent"]
        )
        territori[nome] = territorio

    return territori
