import random
import itertools

SECTORS = ["Вода", "Дерево", "Металл", "Земля"]
NUM_TEAMS = 12
POPULATION_SIZE = 100
MAX_GENERATIONS = 1000
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.1


def generate_individual():
    return random.sample(range(NUM_TEAMS), NUM_TEAMS)


def calculate_fitness(individual):
    fitness = 0
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            if individual[i] == individual[j]:
                break
            fitness += 1
    return fitness


def crossover(individual1, individual2):
    crossover_point = random.randint(1, NUM_TEAMS - 1)
    offspring1 = individual1[:crossover_point] + [x for x in individual2 if x not in individual1[:crossover_point]]
    offspring2 = individual2[:crossover_point] + [x for x in individual1 if x not in individual2[:crossover_point]]
    return offspring1, offspring2


def mutate(individual):
    if random.random() < MUTATION_PROBABILITY:
        i1, i2 = random.sample(range(NUM_TEAMS), 2)
        individual[i1], individual[i2] = individual[i2], individual[i1]
    return individual


def run_genetic_algorithm():
    population = [generate_individual() for _ in range(POPULATION_SIZE)]
    new_population = []

    for generation in range(MAX_GENERATIONS):

        fitnesses = [calculate_fitness(individual) for individual in population]
        sorted_population = [population[i] for i in sorted(range(len(fitnesses)), key=lambda k: fitnesses[k])][-POPULATION_SIZE:]

        if 0 in fitnesses:
            return list(itertools.permutations(range(NUM_TEAMS)))

        while len(new_population) < POPULATION_SIZE:
            individuals = random.choices(
                sorted_population, k=2, weights=[fitness ** 2 for fitness in [calculate_fitness(individual) for individual in sorted_population]]
            )
            individual1, individual2 = individuals

            if random.random() < CROSSOVER_PROBABILITY:
                offspring1, offspring2 = crossover(individual1, individual2)
                new_population.append(mutate(offspring1))
                new_population.append(mutate(offspring2))
            else:
                new_population.append(mutate(individual1))
                new_population.append(mutate(individual2))

        population = new_population[:]
        new_population.clear()

    return list(itertools.permutations(range(NUM_TEAMS)))


schedules = run_genetic_algorithm()

for i, schedule in enumerate(schedules):
    print(f"Schedule {i}:")
    for j, sector in enumerate(SECTORS):
        print(f"{sector}: {schedule[j * NUM_TEAMS // len(SECTORS):(j + 1) * NUM_TEAMS // len(SECTORS)]}")
    print()
