from Classes import Chromosome


class Result:

    def __init__(self,
                 seed: int,
                 generations: int,
                 time: float,
                 population: int,
                 mutation_prob: float,
                 crossover_prob: float,
                 best_ddap: int,
                 best_dap: int,
                 best_chromosome: Chromosome,
                 link_load_list,
                 link_size_list):
        self.seed = seed
        self.generations = generations
        self.time = time
        self.population = population
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.best_ddap = best_ddap
        self.best_dap = best_dap
        self.best_chromosome = best_chromosome
        self.link_load_list = link_load_list
        self.link_size_list = link_size_list

    def get_strings(self):
        strings = [
            "Seed:\t\t\t\t\t\t{}".format(self.seed),
            "Generations:\t\t\t\t{}".format(self.generations),
            "Time elapsed:\t\t\t\t{}".format(self.time),
            "Initial population size:\t{}".format(self.population),
            "Mutation probability:\t\t{}".format(self.mutation_prob),
            "Crossover probability multiplier:\t\t{}".format(self.crossover_prob),
            "Best DDAP fitness:\t\t\t{}".format(self.best_ddap),
            "Best DAP fitness:\t\t\t{}".format(self.best_dap),
            "\nBest chromosome:"
        ]
        d = 0
        for gene in self.best_chromosome.list_of_genes:
            d += 1
            strings.append("Demand {}: {}".format(d, str(gene.path_flow_list)))
        strings.append("Link loads (\"number of signals\"):")
        strings.append(str(self.link_load_list))
        strings.append("Link sizes (\"number of fibers\"):")
        strings.append(str(self.link_size_list))
        return strings

    def print(self):
        for line in self.get_strings():
            print(line)

    def file_write(self):
        result_file = open("results.txt", "w")
        for line in self.get_strings():
            result_file.write(line+"\n")
        result_file.close()
