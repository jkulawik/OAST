class Result:

    def __init__(self,
                 seed: int,
                 generations: int,
                 time: float,
                 population: int,
                 mutation_prob: float,
                 crossover_prob: float,
                 best_ddap: int,
                 best_dap: int):
        self.seed = seed
        self.generations = generations
        self.time = time
        self.population = population
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.best_ddap = best_ddap
        self.best_dap = best_dap

    def get_strings(self):
        strings = [
            "Seed:\t\t\t\t\t\t{}".format(self.seed),
            "Generations:\t\t\t\t{}".format(self.generations),
            "Time elapsed:\t\t\t\t{}".format(self.time),
            "Initial population size:\t{}".format(self.population),
            "Mutation probability:\t\t{}".format(self.mutation_prob),
            "Crossover probability:\t\t{}".format(self.crossover_prob),
            "Best DDAP fitness:\t\t\t{}".format(self.best_ddap),
            "Best DAP fitness:\t\t\t{}".format(self.best_dap)
        ]
        return strings

    def print(self):
        for line in self.get_strings():
            print(line)

    def file_write(self):
        result_file = open("results.txt", "w")
        for line in self.get_strings():
            result_file.write(line+"\n")
        result_file.close()
