import random

# ----------------------------
#  Données : activités Madagascar
# ----------------------------
activites = [
    {"nom": "Hôtel à Tana", "cout": 30, "plaisir": 6, "type": "repos", "duree": 1, "ville": "Tana", "categorie": "détente"},
    {"nom": "Visite Avenue Indépendance", "cout": 0, "plaisir": 5, "type": "culture", "duree": 0.5, "ville": "Tana", "categorie": "culture"},
    {"nom": "Marché artisanal", "cout": 5, "plaisir": 6, "type": "culture", "duree": 0.5, "ville": "Tana", "categorie": "culture"},
    {"nom": "Parc Andasibe", "cout": 40, "plaisir": 9, "type": "nature", "duree": 1, "ville": "Andasibe", "categorie": "aventure"},
    {"nom": "Allée des Baobabs", "cout": 30, "plaisir": 9, "type": "nature", "duree": 1, "ville": "Morondava", "categorie": "aventure"},
    {"nom": "Hôtel à Nosy Be", "cout": 60, "plaisir": 8, "type": "repos", "duree": 1, "ville": "Nosy Be", "categorie": "détente"},
    {"nom": "Plage à Nosy Be", "cout": 20, "plaisir": 9, "type": "repos", "duree": 1, "ville": "Nosy Be", "categorie": "détente"},
    {"nom": "Plongée", "cout": 50, "plaisir": 10, "type": "aventure", "duree": 1, "ville": "Nosy Be", "categorie": "aventure"},
    {"nom": "Restaurant local", "cout": 10, "plaisir": 7, "type": "food", "duree": 0.5, "ville": "Tana", "categorie": "économique"},
]

# ----------------------------
#  Transport entre villes (coût € et durée en jours)
# ----------------------------
transport = {
    ("Tana", "Nosy Be"): {"cout": 50, "duree": 0.5},
    ("Tana", "Morondava"): {"cout": 40, "duree": 0.5},
    ("Nosy Be", "Morondava"): {"cout": 60, "duree": 0.5},
}
# Symétrique
for (v1, v2), val in list(transport.items()):
    transport[(v2, v1)] = val

# ----------------------------
#  Paramètres utilisateur
# ----------------------------
BUDGET = 150
DUREE_MAX = 3
POPULATION_SIZE = 30
GENERATIONS = 60
MUTATION_RATE = 0.1

# ----------------------------
#  Génération d’un individu
# ----------------------------
def creer_individu():
    return [random.randint(0, 1) for _ in range(len(activites))]

# ----------------------------
#  Fitness améliorée
# ----------------------------
def fitness(individu):
    total_cout = 0
    total_duree = 0
    total_plaisir = 0
    villes = []
    types = set()
    dernier_ville = None

    for i in range(len(individu)):
        if individu[i] == 1:
            act = activites[i]
            # transport si changement de ville
            if dernier_ville and act["ville"] != dernier_ville:
                trans = transport.get((dernier_ville, act["ville"]), {"cout":50, "duree":0.5})
                total_cout += trans["cout"]
                total_duree += trans["duree"]
            total_cout += act["cout"]
            total_duree += act["duree"]
            total_plaisir += act["plaisir"]
            types.add(act["categorie"])
            villes.append(act["ville"])
            dernier_ville = act["ville"]

    penalite = 0
    # pénalité budget
    if total_cout > BUDGET:
        penalite += (total_cout - BUDGET) * 2
    # pénalité durée
    if total_duree > DUREE_MAX:
        penalite += (total_duree - DUREE_MAX) * 2
    # pénalité trop de villes
    if len(set(villes)) > 3:
        penalite += (len(set(villes)) -3) * 20

    # bonus diversité catégorie
    bonus = len(types) * 2

    return total_plaisir + bonus - penalite

# ----------------------------
#  Sélection
# ----------------------------
def selection(population):
    population = sorted(population, key=lambda x: fitness(x), reverse=True)
    return population[:len(population)//2]

# ----------------------------
#  Croisement
# ----------------------------
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1)-1)
    enfant = parent1[:point] + parent2[point:]
    return enfant

# ----------------------------
#  Mutation
# ----------------------------
def mutation(individu):
    for i in range(len(individu)):
        if random.random() < MUTATION_RATE:
            individu[i] = 1 - individu[i]
    return individu

# ----------------------------
#  Algorithme génétique
# ----------------------------
def algo_genetique():
    population = [creer_individu() for _ in range(POPULATION_SIZE)]

    for _ in range(GENERATIONS):
        population = selection(population)
        nouvelle_population = []

        while len(nouvelle_population) < POPULATION_SIZE:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            enfant = crossover(parent1, parent2)
            enfant = mutation(enfant)
            nouvelle_population.append(enfant)

        population = nouvelle_population

    return sorted(population, key=lambda x: fitness(x), reverse=True)

# ----------------------------
#  Affichage des plans
# ----------------------------
def afficher_solution(individu):
    total_cout = 0
    total_duree = 0
    dernier_ville = None

    print("\n Plan de voyage :")
    for i in range(len(individu)):
        if individu[i] == 1:
            act = activites[i]
            if dernier_ville and act["ville"] != dernier_ville:
                trans = transport.get((dernier_ville, act["ville"]), {"cout":50, "duree":0.5})
                print(f"  🚗 Transport {dernier_ville} → {act['ville']} ({trans['cout']}€, {trans['duree']}j)")
                total_cout += trans["cout"]
                total_duree += trans["duree"]
            print(f"- {act['nom']} ({act['cout']}€, {act['duree']}j, {act['ville']}) [{act['categorie']}]")
            total_cout += act["cout"]
            total_duree += act["duree"]
            dernier_ville = act["ville"]

    print(f" Coût total : {total_cout}€")
    print(f" Durée totale : {total_duree} jours")
    print(f" Score : {fitness(individu)}")

# ----------------------------
#  Filtrer par catégorie
# ----------------------------
def filtrer_par_categorie(solution, categorie):
    return [activites[i]["nom"] for i, val in enumerate(solution) if val == 1 and activites[i]["categorie"] == categorie]

# ----------------------------
#  Lancement
# ----------------------------
resultats = algo_genetique()

print("\n TOP 3 PLANS :")
for i in range(3):
    afficher_solution(resultats[i])
    # Afficher suggestions par catégorie
    print("   Suggestions Aventure :", filtrer_par_categorie(resultats[i], "aventure"))
    print("   Suggestions Détente :", filtrer_par_categorie(resultats[i], "détente"))
    print("   Suggestions Économique :", filtrer_par_categorie(resultats[i], "économique"))