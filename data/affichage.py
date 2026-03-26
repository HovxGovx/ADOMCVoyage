from data.activites import activites
from data.transport import transport
from ga.fitness import fitness

def afficher_individu(individu):
    total_cout = 0
    total_duree = 0
    last_city = None

    print("\nPlan de voyage")

    for i in range(len(individu)):
        if individu[i] == 1:
            act = activites[i]

            if last_city and act["ville"] != last_city:
                t = transport.get((last_city, act["ville"]), {"cout":50, "duree":0.5})
                print(f"Transport {last_city} -> {act['ville']} ({t['cout']}€, {t['duree']}j)")
                total_cout += t["cout"]
                total_duree += t["duree"]

            print(f"{act['nom']} - {act['ville']} ({act['cout']}€, {act['duree']}j)")
            total_cout += act["cout"]
            total_duree += act["duree"]

            last_city = act["ville"]

    print(f"Cout total: {total_cout}")
    print(f"Duree totale: {total_duree}")
    print(f"Score: {fitness(individu)}")