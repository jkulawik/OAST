import oast_parser
import EvolutionaryAlgorithm
import random
import time


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
time = 0
number_of_generations = 0
number_of_mutations = 0
not_improved_in_N_generations = 0

network = ''


# Input phase
while True:
    net_input = input("[1] net4.txt\n"
                      "[2] net12_1.txt\n"
                      "[3] net12_2.txt\n"
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
    else:
        print("You have to choose number 1-3!")

initial_population = input("Type initial population:\t")
mutation_probability = input("Type mutation probability:\t")
crossover_probability = input("Type crossover probability:\t")

while True:
    stop_input = input("[1] number of seconds\n"
                       "[2] number of generations\n"
                       "[3] number of mutations\n"
                       "[4] not improved in N generations\n"
                       "Choose stop criterion:\t")

    if stop_input == "1":
        time = int(input("How many seconds?:\t"))
        break
    elif stop_input == "2":
        number_of_generations = int(input("How many generations?:\t"))
        break
    elif stop_input == "3":
        number_of_mutations = int(input("How many mutations?:\t"))
        break
    elif stop_input == "4":
        not_improved_in_N_generations = int(input("How many generations when not improved?:\t"))
        break
    else:
        print("You have to choose number 1-4!")


#network = "net12_1.txt"

# Calculate phase
with open(network, "r") as network_file:

    # Get parameters from file
    links_list = oast_parser.get_links(network)
    demand_list = oast_parser.get_demands(network)

    first_population = EvolutionaryAlgorithm.generate_first_population(demand_list, initial_population)
    current_population = first_population

    EvolutionaryAlgorithm.calculate_fitness(links_list, demand_list, current_population)

    for i in first_population:
        for gene in i.list_of_genes:
            print(gene.path_flow_list)
        print("DAP:" + str(i.fitness_dap))
        print("DDAP:" + str(i.fitness_ddap))








