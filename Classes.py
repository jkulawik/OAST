import random

class Link:

    def __init__(self, start_node, end_node, number_of_modules, module_cost, link_module):
        self.start_node = start_node  # ID int
        self.end_node = end_node  # ID int
        self.number_of_modules = number_of_modules  # int; number of modules installed on link
        self.module_cost = module_cost  # int
        self.link_module = link_module  # int (in demand units, e.g. Mbps)

    # Debug
    def print(self):
        print("Start node: {}, End node: {}, Number of modules: {}, Module cost: {}, Link module: {}"
              .format(self.start_node,
                      self.end_node,
                      self.number_of_modules,
                      self.module_cost,
                      self.link_module))


class Demand:

    def __init__(self, start_node, end_node, demand_volume, number_of_demand_paths, list_of_demand_paths):
        self.start_node = start_node  # as String
        self.end_node = end_node  # as String
        self.demand_volume = demand_volume  # as Int
        self.number_of_demand_paths = number_of_demand_paths  # as Int
        self.list_of_demand_paths = list_of_demand_paths  # First item at position 0

    # Debug
    def print(self):
        print("Start node: {}, End node: {}, Demand volume: {}\nNumber of demand paths: {}"
              .format(self.start_node,
                      self.end_node,
                      self.demand_volume,
                      self.number_of_demand_paths))
        for i in range(0, self.number_of_demand_paths):
            self.list_of_demand_paths[i].print()


class DemandPath:

    def __init__(self, demand_path_id, link_id_list):
        self.demand_path_id = demand_path_id  # int
        self.link_id_list = link_id_list  # List of link IDs (Strings) that construct demand path

    # Debug
    def print(self):
        print("\t\tDemand path ID: {}, Demand path links IDs list: {}".format(
            self.demand_path_id,
            self.link_id_list))


# A gene encodes an allocation pattern for a demand
# It holds variables (path flows) of each demand path
# The demand volume is same as in a demand
# Sum of path flows must equal demand volume (which is taken from the demand)
class Gene:

    def __init__(self, path_flow_list, demand_volume):
        self.path_flow_list = path_flow_list  # list of int
        # Sum of all values on list of path flows should be the same as demand_volume
        self.demand_volume = demand_volume  # int


# A chromosome holds genes, one for each given demand
# It encodes a complete feasible solution
class Chromosome:

    def __init__(self, list_of_genes, fitness_dap, fitness_ddap):
        self.list_of_genes = list_of_genes  # as list of Int
        self.fitness_dap = fitness_dap  # int; biggest link overload
        self.fitness_ddap = fitness_ddap  # int; sum of link costs
        # Fitness function = the objective function
