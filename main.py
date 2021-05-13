import math
from matplotlib import pyplot
from Result import Result
import oast_parser
import EvolutionaryAlgorithm
import time
import random
from Classes import Chromosome

# DAP: find allocation of path flows that minimizes the max load function.
# link capacity = link module * number of modules
# link overload = the sum of path flows (across all demands and paths) - link capacity
# each link has its own link overload
# Max load function = biggest link overload
# Objective: minimize the max load function, i.e. lower all link overloads as much as possible.

# DDAP: find allocation of path flows that minimizes the cost of links
# link load = the sum of path flows (across all demands and paths)
# link size = ceiling( link load / link module )
# link cost = module cost * link size
# Minimize the sum of link costs

# init algorithm parameters
not_improved_in_N_generations = 0
initial_population_size = 10
mutation_probability = 0.03
crossover_probability_mul = 0.9
seed = 16418368
random.seed(seed)

EvolutionaryAlgorithm.algorithm = "DDAP"
network = "nets/net4.txt"
stop_input = "1"
max_number_of_seconds = 10
max_number_of_generations = 20
max_number_of_mutations = 100
max_unimproved_generations = 10

# counters
generations_counter = 0
time_elapsed = 0
mutations_counter = 0
not_improved_counter = 0


def check_if_stop(elapsed_time, generations, mutations, unimproved_generations):
    if stop_input == "1":
        return elapsed_time <= max_number_of_seconds
    elif stop_input == "2":
        return generations <= max_number_of_generations
    elif stop_input == "3":
        return mutations <= max_number_of_mutations
    elif stop_input == "4":
        return unimproved_generations <= max_unimproved_generations


# "MAIN":

# Input phase
# TODO pick DDAP or DAP

while True:
    net_input = input("[1] net4.txt\n"
                      "[2] net12_1.txt\n"
                      "[3] net12_2.txt\n"
                      "[s] Skip manual input and use script defaults\n"
                      "Choose network topology txt file:\t")
    if net_input == "1":
        network = "nets/net4.txt"
        break
    elif net_input == "2":
        network = "nets/net12_1.txt"
        break
    elif net_input == "3":
        network = "nets/net12_2.txt"
        break
    elif net_input == "s":
        # Default values from init (top of the file) are kept
        break
    else:
        print("You have to choose number 1-3 or 's'!")

if net_input != "s":

    initial_population_size = int(input("Type initial population:\t"))
    mutation_probability = float(input("Type mutation probability:\t"))
    crossover_probability_mul = float(input("Type crossover probability multiplier:\t"))

    while True:
        stop_input = input("[1] number of seconds\n"
                           "[2] number of generations\n"
                           "[3] number of mutations\n"
                           "[4] not improved in N generations\n"
                           "Choose stop criterion:\t")

        if stop_input == "1":
            max_number_of_seconds = float(input("How many seconds?:\t"))
            break
        elif stop_input == "2":
            max_number_of_generations = int(input("How many generations?:\t"))
            break
        elif stop_input == "3":
            max_number_of_mutations = int(input("How many mutations?:\t"))
            break
        elif stop_input == "4":
            max_unimproved_generations = int(input("How many generations when not improved?:\t"))
            break
        else:
            print("You have to choose number 1-4!")
else:
    # this means s[kip] was chosen; keep default values
    pass

# The calculations proper:
with open(network, "r") as network_file:
    start_time = time.time()

    # Get parameters from file
    links_list = oast_parser.get_links(network)
    demand_list = oast_parser.get_demands(network)

    # Init population
    current_population = EvolutionaryAlgorithm.generate_first_population(demand_list, initial_population_size)
    EvolutionaryAlgorithm.calculate_fitness(links_list, demand_list, current_population)
    # Sort population
    if EvolutionaryAlgorithm.algorithm == "DDAP":
        current_population.sort(key=lambda x: x.fitness_ddap, reverse=False)
    else:
        current_population.sort(key=lambda x: x.fitness_dap, reverse=False)

    # Init references for DDAP results
    best_ddap_chromosome = current_population[0]
    best_ddap_chromosomes = list()  # Trajectory
    best_ddap_chromosomes.append(best_ddap_chromosome)
    best_ddap = math.inf

    # Init references for DAP results
    best_dap_chromosome = current_population[0]
    best_dap_chromosomes = list()  # Trajectory
    best_dap_chromosomes.append(best_dap_chromosome)
    best_dap = math.inf

    # For trajectory graph:
    best_fitness_list = list()
    best_generations = list()  # X values for graph

    # Stores the prioritised fitness
    current_fitness = 0
    best_fitness = 0

    while check_if_stop(time_elapsed, generations_counter, mutations_counter, not_improved_counter):
        # Pick which fitness to prioritise based on chosen algorithm, then recalc the relevant parameters
        if EvolutionaryAlgorithm.algorithm == "DDAP":
            current_ddap = current_population[0].fitness_ddap

            if current_ddap < best_ddap:
                best_ddap_chromosome = current_population[0]
                best_ddap = current_population[0].fitness_ddap
                best_ddap_chromosomes.append(best_ddap_chromosome)
                # Store trajectory
                best_generations.append(generations_counter)
                best_fitness_list.append(best_ddap_chromosome.fitness_ddap)

            current_fitness = current_ddap
            best_fitness = best_ddap
        else:  # DAP
            current_dap = current_population[0].fitness_dap

            if current_dap < best_dap:
                best_dap_chromosome = current_population[0]
                best_dap = current_population[0].fitness_dap
                best_dap_chromosomes.append(best_dap_chromosome)
                # Store trajectory
                best_generations.append(generations_counter)
                best_fitness_list.append(best_dap_chromosome.fitness_dap)

            current_fitness = current_dap
            best_fitness = best_dap

        # Crossover and recalc fitness'
        new_population = EvolutionaryAlgorithm.crossover_chromosomes(
            current_population,
            current_fitness,
            crossover_probability_mul)
        EvolutionaryAlgorithm.calculate_fitness(links_list, demand_list, new_population)

        # Mutate and recalc fitness'
        for chromosome in new_population:
            EvolutionaryAlgorithm.mutate_chromosome(chromosome, mutation_probability)
            mutations_counter += 1
        EvolutionaryAlgorithm.calculate_fitness(links_list, demand_list, new_population)

        # Sort population
        if EvolutionaryAlgorithm.algorithm == "DDAP":
            new_population.sort(key=lambda x: x.fitness_ddap, reverse=False)
        else:
            new_population.sort(key=lambda x: x.fitness_dap, reverse=False)

        # Calculate the remaining counters:
        if EvolutionaryAlgorithm.algorithm == "DDAP":
            if new_population[0].fitness_ddap <= best_ddap:
                not_improved_counter += 1
        else:
            if new_population[0].fitness_dap <= best_dap:
                not_improved_counter += 1
        generations_counter += 1
        time_elapsed = time.time() - start_time

        # Keep n=initial_population_size best chromosomes, discard rest
        tmp = new_population[:initial_population_size]
        current_population = tmp

# Loop finished: process results
best_chromosome: Chromosome
if EvolutionaryAlgorithm.algorithm == "DDAP":
    best_chromosome = best_ddap_chromosome
else:
    best_chromosome = best_dap_chromosome

link_loads = EvolutionaryAlgorithm.get_link_loads(best_chromosome, links_list, demand_list)
link_sizes = EvolutionaryAlgorithm.get_link_sizes(link_loads, links_list)

result = Result(
    seed=seed,
    generations=generations_counter,
    time=time_elapsed,
    population=initial_population_size,
    mutation_prob=mutation_probability,
    crossover_prob=crossover_probability_mul,
    best_ddap=best_ddap,
    best_dap=best_dap,
    best_chromosome=best_chromosome,
    link_load_list=link_loads,
    link_size_list=link_sizes
)

result.print()
result.file_write()


# Graph
pyplot.plot(best_generations, best_fitness_list, 'o-g')
pyplot.xlabel("Generation")
pyplot.ylabel("Best chromosome fitness")
pyplot.title("Optimization Trajectory - "+EvolutionaryAlgorithm.algorithm)
pyplot.show()
