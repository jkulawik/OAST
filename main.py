import oast_parser
import EvolutionaryAlgorithm
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
max_number_of_generations = 0
max_number_of_mutations = 0
not_improved_in_N_generations = 0
network = ""
stop_input = ""

# counters
time_elapsed = 0
generations_counter = 0
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
while True:
    net_input = input("[1] net4.txt\n"
                      "[2] net12_1.txt\n"
                      "[3] net12_2.txt\n"
                      "[T] Test: all parameters from script\n"
                      "Choose network topology txt file:\t")
    if net_input == "T":
        break
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

network = "nets/net4.txt"
initial_population_size = 3
mutation_probability = 0.1

stop_input = "1"
max_number_of_seconds = 3
max_number_of_generations = 5
max_number_of_mutations = 10
max_unimproved_generations = 10

if net_input != "T":
    initial_population_size = int(input("Type initial population:\t"))
    mutation_probability = int(input("Type mutation probability:\t"))

    while True:
        stop_input = input("[1] number of seconds\n"
                           "[2] number of generations\n"
                           "[3] number of mutations\n"
                           "[4] not improved in N generations\n"
                           "Choose stop criterion:\t")

        if stop_input == "1":
            max_number_of_seconds = input("How many seconds?:\t")
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
    # this means T[est] was chosen; keep default values
    pass

#print("Stop cryterium: ", stop_input)
print("Max time: ", max_number_of_seconds)

# The calculations proper:
with open(network, "r") as network_file:

    # Get parameters from file
    links_list = oast_parser.get_links(network)
    demand_list = oast_parser.get_demands(network)

    first_population = EvolutionaryAlgorithm.generate_first_population(demand_list, initial_population_size)
    current_population = first_population

    EvolutionaryAlgorithm.calculate_fitness(links_list, demand_list, current_population)

    #for i in first_population:
    #    print("Current chromosome genes:\n")
    #    for gene in i.list_of_genes:
    #        print(gene.path_flow_list)
    #    print("DAP:" + str(i.fitness_dap))
    #    print("DDAP:" + str(i.fitness_ddap))

    start_time = time.time()
    while check_if_stop(time_elapsed, generations_counter, mutations_counter, not_improved_counter):
        # current parameters

        current_ddap = current_population[0].fitness_ddap
        current_dap = current_population[0].fitness_dap
        print("Current DDAP fitness: ", current_ddap)

        new_population = EvolutionaryAlgorithm.crossover_chromosomes(current_population, current_ddap)
        #input("Press Enter to continue")

        for chromosome in new_population:
            EvolutionaryAlgorithm.mutate_chromosome(chromosome, mutation_probability)
            mutations_counter += 1

        # TODO: The best ddap fitness can go down for some reason. Fix this
        EvolutionaryAlgorithm.calculate_fitness(links_list, demand_list, new_population)
        new_population.sort(key=lambda x: x.fitness_ddap, reverse=False)  # TODO change for DAP when needed

        # Calculate the remaining counters:
        if new_population[1].fitness_ddap <= current_ddap and new_population[1].fitness_dap <= current_dap:  # TODO tu nie powinno być [0]?
            not_improved_counter += 1
        generations_counter += 1
        end_time = time.time()
        time_elapsed = end_time - start_time

        # Keep n=initial_population_size best chromosomes, discard rest
        tmp = new_population[:initial_population_size]
        current_population = tmp
