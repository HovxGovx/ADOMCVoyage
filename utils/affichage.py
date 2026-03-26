from data.activites import activites
from data.transport import transport
from ga.fitness import fitness

def afficher_individu(individu):
    total_cout = 0
    total_duree = 0
    last_city= None
    print("\n Plan de voyage :")
    for i in range (len(individu)):
        if individu[i] == 1:
            act = activites[i]
            if last_city and act["ville"] != last_city:
                t= transport.get((last_city, act["ville"]), {"cout":50, "duree":0.5})
                total_cout += t["cout"]
                total_duree += t["duree"]
                print(f"  - Transport de {last_city} à {act['ville']} : coût {t['cout']}€, durée {t['duree']}h")
            print(f"  - {act['type'].capitalize()} à {act['ville']} : coût {act['cout']}€, durée {act['duree']}h, plaisir {act['plaisir']}")
            total_cout += act["cout"]
            total_duree += act["duree"]
            last_city = act["ville"]
        print(f"\n Coût total : {total_cout}€, Durée totale : {total_duree}h, Fitness : {fitness(individu)}")