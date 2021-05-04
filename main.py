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
time = 0  # TODO to chyba psuje kod dalej
number_of_generations = 0
number_of_mutations = 0
not_improved_in_N_generations = 0
network = ""
stop_input = ""

# counters
time_elapsed = 0
generations_counter = 0
mutations_counter = 0
not_improved_counter = 0

# TODO NIE JESTEM PEWIEN CZY ZADZIALA
def stop_function(fitness_time, fitness_generations, fitness_mutations, fitness_not_improved):
    if stop_input == "1" and fitness_time <= number_of_seconds:
        return False
    elif stop_input == "2" and fitness_generations <= number_of_generations:
        return False
    elif stop_input == "3" and fitness_mutations <= number_of_mutations:
        return False
    elif stop_input == "4" and fitness_not_improved <= not_improved_in_N_generations:
        return False
    else:
        return True


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

if net_input != "T":
    initial_population = int(input("Type initial population:\t"))
    mutation_probability = int(input("Type mutation probability:\t"))
    crossover_probability = int(input("Type crossover probability:\t"))

    while True:
        stop_input = input("[1] number of seconds\n"
                           "[2] number of generations\n"
                           "[3] number of mutations\n"
                           "[4] not improved in N generations\n"
                           "Choose stop criterion:\t")

        if stop_input == "1":
            number_of_seconds = int(input("How many seconds?:\t"))
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
else:
    # this means T[est] was chosen
    network = "nets/net4.txt"
    initial_population = 3
    mutation_probability = 0.1
    crossover_probability = 0.1

    stop_input = 1
    number_of_seconds = 3
    number_of_generations = 5
    number_of_mutations = 10
    not_improved_in_N_generations = 10


# Calculate phase
with open(network, "r") as network_file:

    # Get parameters from file
    links_list = oast_parser.get_links(network)
    demand_list = oast_parser.get_demands(network)

    first_population = EvolutionaryAlgorithm.generate_first_population(demand_list, initial_population)
    current_population = first_population

    EvolutionaryAlgorithm.calculate_fitness(links_list, demand_list, current_population)

    #for i in first_population:
    #    print("Current chromosome genes:\n")
    #    for gene in i.list_of_genes:
    #        print(gene.path_flow_list)
    #    print("DAP:" + str(i.fitness_dap))
    #    print("DDAP:" + str(i.fitness_ddap))

    while stop_function(time_elapsed, generations_counter, mutations_counter, not_improved_counter):

        # current parameters
        start_time = time.time()
        current_ddap = current_population[0].fitness_ddap
        current_dap = current_population[0].fitness_dap

        new_population = EvolutionaryAlgorithm.crossover_chromosomes(current_population, crossover_probability)
        for chromosome in new_population:
            if EvolutionaryAlgorithm.mutate_chromosome(chromosome, mutation_probability):
                mutations_counter += 1

        EvolutionaryAlgorithm.calculate_fitness(links_list, demand_list, new_population)
        new_population.sort(key=lambda x: x.fitness_ddap)

        if new_population[1].fitness_ddap <= current_ddap and new_population[1].fitness_dap <= current_dap:
            not_improved_counter += 1

        tmp = new_population[:initial_population]  # TODO NA CO TO KOMU ???
        current_population = tmp

        generations_counter += 1

        end_time = time.time()
        time_elapsed = end_time - start_time
