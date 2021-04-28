
import oast_parser

oast_parser.get_links()
#oast_parser.get_demands()

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
