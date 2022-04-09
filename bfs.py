import sys


def get_nodelist(adj_list):
    """Gets a list of all nodes in the graph represented by a given adjacency list."""
    keys_list = (list(adj_list.keys()))
    nodes_list = []
    for key in keys_list:
        if key not in nodes_list:
            nodes_list.append(key)
        edge_list = adj_list[key]
        for dest in edge_list:
            if dest not in nodes_list:
                nodes_list.append(dest)
    return nodes_list


def get_adj_matrix_entry(adj_matrix, i, j):
    """Gets an entry in the given adjacency matrix.

    This exists to make sure data is only in one place per edge, even for an undirected graph.
    Data is read from the top right half of the matrix."""
    if i > j:  # swap coordinates if i>j
        k = i
        i = j
        j = k
    return adj_matrix[i][j]


def set_adj_matrix_entry(adj_matrix, i, j, value):
    """Gets an entry in the given adjacency matrix.

    This exists to make sure data is only in one place per edge, even for an undirected graph.
    Data is written to the top right half of the matrix."""
    if i > j:  # swap coordinates if i>j
        k = i
        i = j
        j = k
    adj_matrix[i][j] = value


def map_nodes_to_indices(keys_list):
    """Creates a dictionary mapping node names to their indices in the given list."""
    nodes_to_indices = {}  # for constant-time lookup of index in adj matrix for a given word

    i = 0
    for key in keys_list:
        if key not in nodes_to_indices.keys():
            nodes_to_indices[key] = i
            i += 1

    return nodes_to_indices


def adj_list_to_matrix(adj_list, keys_list, nodes_to_indices):
    """Converts the given adjacency list to an adjacency matrix.

    Nodes are placed in columns/rows according to their indices in nodes_to_indices."""
    nkeys = len(nodes_to_indices.keys())

    adj_matrix = []

    for i in range(nkeys):
        nodes_to_indices[keys_list[i]] = i

    for i in range(nkeys):
        adj_matrix.append([])
        for j in range(nkeys):
            (adj_matrix[-1]).append(0)

    for key in adj_list.keys():
        edge_list = adj_list[key]
        for dest in edge_list:
            set_adj_matrix_entry(adj_matrix, nodes_to_indices[key], nodes_to_indices[dest], 1)

    return adj_matrix


def bfs(start_node, adj_matrix, node_count):
    """Iterative implementation of BFS to obtain distances to all nodes from start_node.

    Distances are saved into the adjacency matrix."""
    node_visited_status = []
    for i in range(node_count):
        node_visited_status.append(0)

    nodes_to_visit = [(start_node, None)]  # queue

    while len(nodes_to_visit) > 0:  # iterative not recursive to avoid extreme recursion depth
        node = nodes_to_visit[0][0]
        prev_node = nodes_to_visit[0][1]
        nodes_to_visit = nodes_to_visit[1:]

        # if node pair not linked by edge and existing distance, if any, is longer
        if prev_node is not None and \
                (get_adj_matrix_entry(adj_matrix, start_node, node) == 0 or
                 get_adj_matrix_entry(adj_matrix, start_node, node) > get_adj_matrix_entry(adj_matrix, start_node,
                                                                                           prev_node) + 1):
            set_adj_matrix_entry(adj_matrix, start_node, node,
                                 get_adj_matrix_entry(adj_matrix, start_node, prev_node) + 1)  # update distance

        for next_node in range(node_count):  # queue child nodes
            if get_adj_matrix_entry(adj_matrix, node, next_node) == 1 and node_visited_status[next_node] != 1:
                nodes_to_visit.append((next_node, node))
                node_visited_status[node] = 1
    return adj_matrix


def bfs_all(adj_matrix, node_count):
    """Runs bfs() starting from each node in the graph iteratively."""
    for i in range(node_count):
        print("Processing node "+str(i)+" of "+str(node_count))
        adj_matrix = bfs(i, adj_matrix, node_count)
    return adj_matrix


def print_adjmatrix(adj_matrix, keys_list):
    """Prints the adjacency matrix to the console for debugging."""
    print("  ", end="")

    for node in keys_list:
        print(str(node) + " ", end="")

    print("\n", end="")

    i = 0

    for row in adj_matrix:
        print(keys_list[i] + " ", end="")
        for col in row:
            print(str(col) + " ", end="")
        print("\n", end="")
        i += 1


def output_distances(adj_matrix):
    """Outputs the distances in CSV format."""
    rownum = 0
    for row in adj_matrix:
        colnum = 0
        for col in row:
            if rownum < colnum and col != 0:
                print(node_list[rownum] + "," + node_list[colnum] + "," + str(col))
            colnum += 1
        rownum += 1


adjlist_input = {}

with open(sys.argv[1]) as f:
    for line in f:
        edge = line.split(",")
        if edge[0].strip() not in adjlist_input:
            adjlist_input[edge[0].strip()] = [edge[1].strip()]
        else:
            adjlist_input[edge[0].strip()].append(edge[1].strip())

node_list = get_nodelist(adjlist_input)

node_index_map = map_nodes_to_indices(node_list)

adjmatrix_input = adj_list_to_matrix(adjlist_input, node_list, node_index_map)

nnodes = len(node_index_map.keys())

adjmatrix_input = bfs_all(adjmatrix_input, nnodes)

output_distances(adjmatrix_input)
