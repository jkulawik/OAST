from Classes import Gene, Chromosome
import random
from math import ceil


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