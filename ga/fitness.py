from data.activites import activites
from data.transport import transport
from config import BUDGET, DUREE_MAX, MAX_VILLES

def fitness(individu):
    total_cout = 0
    total_duree = 0
    total_plaisir = 0

    villes = []
    dernier_ville = None

    for i in range(len(individu)):
        if individu[i] == 1:
            act = activites[i]

            if dernier_ville and act["ville"] != dernier_ville:
                t = transport.get((dernier_ville, act["ville"]), {"cout":50, "duree":0.5})
                total_cout += t["cout"]
                total_duree += t["duree"]

            total_cout += act["cout"]
            total_duree += act["duree"]
            total_plaisir += act["plaisir"]

            villes.append(act["ville"])
            dernier_ville = act["ville"]

    penalite = 0

    if total_cout > BUDGET:
        penalite += (total_cout - BUDGET) * 2

    if total_duree > DUREE_MAX:
        penalite += (total_duree - DUREE_MAX) * 2

    if len(set(villes)) > MAX_VILLES:
        penalite += 50

    # contrainte hotel + restaurant
    for ville in set(villes):
        types = [
            activites[i]["type"]
            for i in range(len(individu))
            if individu[i] == 1 and activites[i]["ville"] == ville
        ]

        if "hotel" not in types:
            penalite += 40

        if "food" not in types:
            penalite += 40

    return total_plaisir - penalite