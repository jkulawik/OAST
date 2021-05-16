from Classes import Link, Demand, DemandPath


def get_links(network_file):
    links = list()
    file = open(network_file, "r")

    # First number in the file is the number of links in the network
    n_links = int(file.readline())

    # For n_links of lines in the file:
    for i in range(n_links):
        # Turn "1 11 2 1 96" into an array: ['1', '11', '2', '1', '96']
        link = file.readline().split()
        # Create a link object:
        link_obj = Link(
            start_node=int(link[0]),
            end_node=int(link[1]),
            number_of_modules=int(link[2]),
            unit_cost=int(link[3]),
            link_module=int(link[4]))
        #link_obj.print()
        links.append(link_obj)

    assert(int(file.readline()) == -1)  # Check for the -1 separator

    file.close()
    return links


def get_demands(network_file):
    demands = list()
    file = open(network_file, "r")
    # Same as with get_links but we do it to skip that part of the file
    n_links = int(file.readline())
    for i in range(n_links):
        file.readline()
    assert (int(file.readline()) == -1)

    file.readline()  # Skip blank line
    n_demands = int(file.readline())

    for i in range(n_demands):
        file.readline()  # Skip blank line
        demand_info = file.readline().split()
        n_of_demand_paths = int(file.readline())
        demand_paths_list = list()

        for j in range(n_of_demand_paths):
            demand_path_info = file.readline().split()
            demand_path_id = int(demand_path_info[0])
            demand_path_info.pop(0)  # Delete demand path ID from array; now only link IDs are inside
            assert(int(demand_path_id) == j+1)  # Check if correct IDs are being read
            demand_path = DemandPath(
                demand_path_id=demand_path_id,
                link_id_list=demand_path_info
            )
            demand_paths_list.append(demand_path)

        demand_obj = Demand(
            start_node=demand_info[0],
            end_node=demand_info[1],
            demand_volume=demand_info[2],
            number_of_demand_paths=n_of_demand_paths,
            list_of_demand_paths=demand_paths_list
        )
        #demand_obj.print()
        demands.append(demand_obj)

    file.close()
    return demands
