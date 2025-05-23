import random


def tira_dadi(num_dadi):
    risultati = [random.randint(1, 6) for _ in range(num_dadi)]
    risultati.sort(reverse=True)
    return risultati


def combattimento(attaccante, difensore, truppe_attaccante, truppe_difensore):
    dadi_attaccante = min(truppe_attaccante, 3)
    dadi_difensore = min(truppe_difensore, 2)

    attacco = tira_dadi(dadi_attaccante)
    difesa = tira_dadi(dadi_difensore)

    perdite_attaccante = 0
    perdite_difensore = 0

    for a, d in zip(attacco, difesa):
        if a > d:
            perdite_difensore += 1
        else:
            perdite_attaccante += 1

    truppe_attaccante_finali = max(truppe_attaccante - perdite_attaccante, 0)
    truppe_difensore_finali = max(truppe_difensore - perdite_difensore, 0)

    return truppe_attaccante_finali, truppe_difensore_finali

