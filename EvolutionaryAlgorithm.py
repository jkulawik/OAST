from Classes import Gene, Chromosome
import random
from math import ceil

DEFAULT_POPULATION_SIZE = 10
DEFAULT_MUTATION_PROBABILITY = 0.01
OFFSPRING_FROM_PARENT_PROBABILITY = 0.5


def generate_chromosome(list_of_demands):
    list_of_genes = list()  # Empty list for appending Genes

    # Generate genes for each demand
    for demand in list_of_demands:
        demand_volume = demand.demand_volume  # Get demand volume for the gene
        number_of_demand_paths = demand.number_of_demand_paths  # Length of the gene

        path_flow_list = [0] * number_of_demand_paths  # Init with zeros

        # Randomly distribute the demand_volume across path flows
        # Sum of path flows must equal demand volume
        for i in range(int(demand_volume)):
            picked_path_flow = random.randint(0, number_of_demand_paths - 1)
            path_flow_list[picked_path_flow] += 1

        new_gene = Gene(path_flow_list, demand_volume)
        list_of_genes.append(new_gene)

    chromosome = Chromosome(list_of_genes, 0, 0)  # Fitness is updated manually in the main script
    return chromosome


def generate_first_population(list_of_demands, population_size: int):
    # Check if first population size is > 0
    if population_size <= 0:
        population_size = DEFAULT_POPULATION_SIZE

    first_population_list = list()
    for i in range(population_size):
        first_population_list.append(generate_chromosome(list_of_demands))
    return first_population_list


# Mutation perturbs the values of the chromosome genes with a certain low probability
def mutate_chromosome(chromosome: Chromosome, mutation_probability: float):

    mutation_probability = check_probability(mutation_probability, DEFAULT_MUTATION_PROBABILITY)

    for gene in chromosome.list_of_genes:
        # For each gene on the list, decide if mutation will be performed
        # Mutation = move 1 unit between 2 path flows in a gene
        if get_random_bool(mutation_probability):
            number_of_path_flows = len(gene.path_flow_list)

            # Randomly select 2 genes to mutate
            first_path_flow_id = random.randint(0, number_of_path_flows - 1)
            second_path_flow_id = random.randint(0, number_of_path_flows - 1)

            # Check if 2nd path flow won't be smaller than 0 after decrementing it
            # and check if the same path flow wasn't chosen for both operations;
            # Get a new 2nd one until the conditions are met
            iterations = 0
            while gene.path_flow_list[second_path_flow_id] < 1 or first_path_flow_id == second_path_flow_id:
                second_path_flow_id = random.randint(0, number_of_path_flows - 1)

                iterations += 1
                if iterations > number_of_path_flows:
                    # We've looped over the whole gene and found no solution; the loop is now soft-locked
                    # Try again with a new first_path_flow_id
                    first_path_flow_id = random.randint(0, number_of_path_flows - 1)
                    # WARNING: THIS CAN STILL SOFT-LOCK

            gene.path_flow_list[first_path_flow_id] += 1
            gene.path_flow_list[second_path_flow_id] -= 1


# Crossover exchanges genes between two parent chromosomes to produce two offspring
# A new population is generated; it includes the old population and all offspring.
def crossover_chromosomes(original_population, biggest_ddap: float):
    # Firstly, list is filled with parent chromosomes
    new_population = list(original_population)

    # Remove 2 parents from the original population until less than 2 left
    while len(original_population) >= 2:
        first_parent_score = original_population[0].fitness_ddap/biggest_ddap  # TODO change for DAP when needed
        first_parent_genes = original_population.pop(0).list_of_genes
        second_parent_score = original_population[0].fitness_ddap/biggest_ddap  # TODO change for DAP when needed
        second_parent_genes = original_population.pop(0).list_of_genes

        # Crossover prob. is determined by parents' fitness
        crossover_probability = (second_parent_score+first_parent_score)/2
        if crossover_probability > 1.0:
            crossover_probability = 1.0

        if get_random_bool(crossover_probability):
            first_offspring_genes = list()
            second_offspring_genes = list()

            # Create offspring from parent genes:
            # For each gene in the parent chromosome...
            for i in range(0, len(first_parent_genes)):
                # First offspring gets gene from first parent, second offspring from second parent
                if get_random_bool(OFFSPRING_FROM_PARENT_PROBABILITY):
                    first_offspring_genes.append(first_parent_genes[i])
                    second_offspring_genes.append(second_parent_genes[i])
                # vice versa as the above:
                else:
                    first_offspring_genes.append(second_parent_genes[i])
                    second_offspring_genes.append(first_parent_genes[i])

            # Add offsprings to the whole list
            first_offspring = Chromosome(first_offspring_genes, 0, 0)
            second_offspring = Chromosome(second_offspring_genes, 0, 0)
            new_population.append(first_offspring)
            new_population.append(second_offspring)
    return new_population


# Calculate fitness for all chromosomes in the passed population (list of chromosomes)
def calculate_fitness(links, demands, population):
    for chromosome in population:
        number_of_links = len(links)
        # Init lists with zeros
        l = [0] * number_of_links  # Link loads
        y = [0] * number_of_links  # Link size (for DDAP)
        f = [0] * number_of_links  # Link overloads (for DAP)
        chromosome.fitness_ddap = 0
        chromosome.fitness_dap = 0
        for d in range(len(chromosome.list_of_genes)):
            for p in range(len(chromosome.list_of_genes[d].path_flow_list)):
                for e in range(len(links)):
                    # Path flow if the edge partakes in the given demand path; else a zero takes the place
                    if check_link_in_demand(e+1, demands[d], p):
                        l[e] += chromosome.list_of_genes[d].path_flow_list[p]
        # At this point we have a list of link loads for each link
        # Now calculate the fitness (objective function value) for both DAP and DDAP:
        for e in range(len(links)):
            y[e] = ceil(l[e]/links[e].link_module)  # Calc link sizes
            f[e] = l[e] - links[e].number_of_modules*links[e].module_cost  # Calc link overloads
            chromosome.fitness_ddap += y[e] * links[e].module_cost
        chromosome.fitness_dap = max(f)


# Check if given link is in a given demand path
def check_link_in_demand(link, demand, path_num):
    demand_path = demand.list_of_demand_paths[path_num]
    return str(link) in demand_path.link_id_list


# Check if possibility is in range between 0 and 1
def check_probability(probability: float, default: float):
    if not 0 <= probability <= 1:
        return default
    else:
        return probability


def get_random_bool(probability: float):
    return random.random() < probability
