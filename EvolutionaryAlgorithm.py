from Classes import Gene, Chromosome
import random
from math import ceil

DEFAULT_MUTATION_PROBABILITY = 0.01
DEFAULT_CROSSOVER_PROBABILITY = 0.1
OFFSPRING_FROM_PARENT_PROBABILITY = 0.5


def get_random_probability(self, probability):
    return random.random() < probability


def generate_chromosome(list_of_demands):
    list_of_genes = list()  # Empty list for appending Genes

    # Generate genes for each demand
    for demand in list_of_demands:
        demand_volume = demand.demand_volume  # Get demand volume for the gene
        number_of_demand_paths = demand.number_of_demand_paths  # Length of the gene

        path_flow_list = [0] * number_of_demand_paths  # Init with zeros

        # Randomly distribute the demand_volume across path flows
        # Sum of path flows must equal demand volume
        for i in range(demand_volume):
            picked_path_flow = random.randint(0, number_of_demand_paths - 1)
            path_flow_list[picked_path_flow] += 1

        new_gene = Gene(path_flow_list, demand_volume)
        list_of_genes.append(new_gene)

    chromosome = Chromosome(list_of_genes, 0, 0)  # Fitness is updated manually in the main script
    return chromosome

def generate_first_population(list_of_demands, population_size):

    first_population_list = list()

    for i in range(population_size):
        first_population_list.append(generate_chromosome(list_of_demands))

    return first_population_list


# Mutation perturbs the values of the chromosome genes with a certain low probability
def mutate_chromosome(chromosome, mutation_probability):

    # Check if possibility is in range between 0 and 1
    if 0 <= mutation_probability <= 1:
        mutation_probability = mutation_probability
    else:
        mutation_probability = DEFAULT_MUTATION_PROBABILITY

    for gene in chromosome.list_of_genes:
        # For each gene on the list, decide if mutation will be performed
        if get_random_probability(mutation_probability):
            number_of_path_flow = len(gene.path_flow_list)

            # Randomly select 2 genes to mutate
            first_gene_to_mutate = random.randint(0, number_of_path_flow - 1)
            second_gene_to_mutate = random.randint(0, number_of_path_flow - 1)

            # Check if chosen path flow is different from 0
            if gene.path_flow_list[first_gene_to_mutate] == 0:
                first_gene_to_mutate = random.randint(0, number_of_path_flow - 1)

            # Check if selected path flows are different
            if gene.path_flow_list[second_gene_to_mutate] == gene.path_flow_list[first_gene_to_mutate]:
                second_gene_to_mutate_gene_to_mutate = random.randint(0, number_of_path_flow - 1)

            gene.path_flow_list[first_gene_to_mutate] += 1
            gene.path_flow_list[second_gene_to_mutate] -= 1

            return True

        else:
            return False

# Crossover exchanges genes between two parent chromosomes to produce two offspring
def crossover_chromosomes(chromosomes_list, crossover_probability):

    # Firstly, list is filled with parent chromosomes
    list_of_parents_and_offsprings = list(chromosomes_list)

    # Check if possibility is in range between 0 and 1
    if 0 <= crossover_probability <= 1:
        mutation_probability = crossover_probability
    else:
        mutation_probability = DEFAULT_CROSSOVER_PROBABILITY

    number_of_chromosomes = len(chromosomes_list)

    while number_of_chromosomes >= 2:       # !!! TO CHYBA SIĘ DA JAKOS LADNIEJ ZAPISAC !!!
        first_parent_genes = chromosomes_list.pop(0).list_of_genes
        second_parent_genes = chromosomes_list.pop(0).list_of_genes

        first_offspring_genes = list()
        second_offspring_genes = list()

        if get_random_probability(crossover_probability):

            # Create offspring from parents genes
            for i in range(first_offspring_genes):
                # First offspring from first parent, second offspring from second parent
                if get_random_probability(OFFSPRING_FROM_PARENT_PROBABILITY):
                    first_offspring_genes.append(first_parent_genes[i])
                    second_offspring_genes.append(second_parent_genes[i])
                # First offspring from second parent, second offspring from first parent
                else:
                    first_offspring_genes.append(second_offspring_genes[i])
                    second_offspring_genes.append(first_offspring_genes[i])

            # Add offsprongs to the whole list
            list_of_parents_and_offsprings.append(Chromosome(first_offspring_genes,0,0))
            list_of_parents_and_offsprings.append(Chromosome(second_offspring_genes,0,0))

    return list_of_parents_and_offsprings


# Calculate fitness for all chromosomes in the passed population (list of chromosomes)
def calculate_fitness(links, demands, population):
    for chromosome in population:
        l = [0 for i in range(len(links))]  # Link loads
        y = [0 for i in range(len(links))]  # Link size (for DDAP)
        f = [0 for i in range(len(links))]  # Link overloads (for DAP)
        chromosome.fitness_ddap = 0
        chromosome.fitness_dap = 0
        for d in range(len(chromosome.list_of_genes)):
            for p in range(len(chromosome.list_of_genes[d].path_flow_list)):
                for e in range(len(links)):
                    tmp = chromosome.list_of_genes[d].path_flow_list[p]  # TODO useless line?
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
