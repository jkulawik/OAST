class Result:

    def __init__(self, seed, generations, time, population, mutation_prob, crossover_prob, best_ddap, best_dap):
        self.seed = seed
        self.generations = generations
        self.time = time
        self.population = population
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.best_ddap = best_ddap
        self.best_dap = best_dap

    def print(self):
        print("Seed:\t\t\t\t\t{}\n"
              "Generations:\t\t\t{}\n"
              "Time elapsed:\t\t\t{}\n"
              "Initial population size:{}\n"
              "Mutation probability:\t{}\n"
              "Crossover probability:\t{}\n"
              "Best DDAP fitness:\t\t{}\n"
              "Best DAP fitness:\t\t{}"
              .format(self.seed,
                      self.generations,
                      self.time,
                      self.population,
                      self.mutation_prob,
                      self.crossover_prob,
                      self.best_ddap,
                      self.best_dap))

    def file_write(self):
        result_file = open("result.txt", "a")
        result_file.write("cos") # TODO nie mam pojecia jak tu zapisac tego self.printa()
        result_file.close()