import random
from data.activites import activites

def creer_individu():
    return [random.randint(0, 1) for _ in range(len(activites))]