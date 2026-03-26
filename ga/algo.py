import random
from models.individu import creer_individu
from ga.fitness import fitness
from config import POPULATION_SIZE, GENERATIONS, MUTATION_RATE

def selection(population):
    population = sorted(population, key=lambda x: fitness(x), reverse=True)
    return population[:len(population)//2]

def crossover(p1,p2):
    point = random.randint(1, len(p1)-1)
    return p1[:point] + p2[point:]

def mutation(individu):
    for i in range(len(individu)):
        if random.random() < MUTATION_RATE:
            individu[i] = 1 - individu[i]
    return individu

def run():
    population = [creer_individu() for _ in range(POPULATION_SIZE)]

    for _ in range(GENERATIONS):
        population = selection(population)
        new_pop = []

        while len(new_pop) < POPULATION_SIZE:
            p1 = random.choice(population)
            p2 = random.choice(population)
            enfant = crossover(p1, p2)
            enfant = mutation(enfant)
            new_pop.append(enfant)

        population = new_pop

    return sorted(population, key=lambda x: fitness(x), reverse=True)