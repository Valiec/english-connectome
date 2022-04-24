import sys
import multiprocessing
from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory

import numpy

DEPTH_LIMIT = 7  # constant
NTHREADS = 8  # constant


class AdjacencyIterator:
    """An iterator for dividing the adjacency matrix into chunks for each process"""
    mat = []  # the adjacency matrix
    ind = 0  # index in the matrix
    chunksize = 0  # the size of chunk to return
    nodecount = 0  # the number of nodes in the graph
    sharedmem_name = None  # name of shared memory block
    sharedmem_shape = None  # shape of array for shared memory
    sharedmem_dtype = None  # data type for shared memory
    nodes_included = None  # the number of nodes actually included in the analysis

    def __init__(self, adj_mat, chunk_size, node_count, included_nodes):
        self.mat = adj_mat
        self.ind = 0
        self.chunksize = chunk_size
        self.node_count = node_count

        # Based on example at
        # https://docs.python.org/3/library/multiprocessing.shared_memory.html#module-multiprocessing.shared_memory

        tmp_numpy_arr = numpy.array(adj_mat)
        sharedmem = SharedMemory(create=True, size=tmp_numpy_arr.nbytes)
        np_arr = numpy.ndarray(tmp_numpy_arr.shape, dtype=tmp_numpy_arr.dtype, buffer=sharedmem.buf)
        np_arr[:] = tmp_numpy_arr[:]

        # store info needed to access shared memory in attributes

        self.sharedmem_name = sharedmem.name
        self.sharedmem_shape = tmp_numpy_arr.shape
        self.sharedmem_dtype = tmp_numpy_arr.dtype
        self.nodes_included = included_nodes

    def __iter__(self):
        return self

    def __next__(self):
        if self.ind < len(self.nodes_included):  # if we aren't already off the end of the list
            csize = self.chunksize
            if self.ind + self.chunksize >= len(
                    self.nodes_included):  # if the chunk would be partly off the end of the list
                csize = len(self.nodes_included) - self.ind  # readjust chunk size to cut off at the end of the list
            self.ind += self.chunksize
            data_tuple = (self.node_count, self.ind - self.chunksize, self.sharedmem_name, self.sharedmem_shape,
                          self.sharedmem_dtype, csize, self.nodes_included)
            return data_tuple  # return big tuple of data
        else:  # off the end
            raise StopIteration


def get_nodelist(adj_list):
    """Gets a list of all nodes in the graph represented by a given adjacency list."""
    keys_list = (list(adj_list.keys()))
    nodes_list = {}
    for key in keys_list:
        nodes_list[key] = 0
        edge_list = adj_list[key]
        for dest in edge_list:
            nodes_list[dest] = 0
    return list(nodes_list.keys())


def get_adj_matrix_entry(adj_matrix, i, j):
    """Gets an entry in the given adjacency matrix.

    This exists to make sure data is only in one place per edge, even for an undirected graph.
    Data is read from the top right half of the matrix."""
    return adj_matrix[i][j] if i < j else adj_matrix[j][i]


def set_adj_matrix_entry(adj_matrix, i, j, value):
    """Gets an entry in the given adjacency matrix.

    This exists to make sure data is only in one place per edge, even for an undirected graph.
    Data is written to the top right half of the matrix."""
    if i < j:
        adj_matrix[i][j] = value
    else:
        adj_matrix[j][i] = value


def map_nodes_to_indices(keys_list):
    """Creates a dictionary mapping node names to their indices in the given list."""
    nodes_to_indices = {}  # for constant-time lookup of index in adj matrix for a given word

    i = 0
    for key in keys_list:
        if key not in nodes_to_indices.keys():
            nodes_to_indices[key] = i
            i += 1

    return nodes_to_indices


def adj_list_to_matrix(adj_list, nodes_to_indices, nodes_included):
    """Converts the given adjacency list to an adjacency matrix.

    Nodes are placed in columns/rows according to their indices in nodes_to_indices."""
    nkeys = len(nodes_to_indices.keys())

    adj_matrix = []

    for i in range(nkeys):
        adj_matrix.append([])
        for j in range(nkeys):
            (adj_matrix[-1]).append(0)

    for key in adj_list.keys():
        edge_list = adj_list[key]
        for dest in edge_list:
            if key in nodes_included and dest in nodes_included:
                set_adj_matrix_entry(adj_matrix, nodes_to_indices[key], nodes_to_indices[dest], 1)

    return adj_matrix


def bfs(start_node, node_count, name, shape, dtype, lock, depth_limit):
    """Iterative implementation of BFS to obtain distances to all nodes from start_node.

    Distances are saved into the adjacency matrix."""

    sharedmem = SharedMemory(name=name)
    adj_mat_global = numpy.ndarray(shape, dtype=dtype, buffer=sharedmem.buf)

    node_visited_status = []
    for i in range(node_count):
        node_visited_status.append(0)

    the_row = []
    for i in range(node_count):
        the_row.append(0)

    nodes_to_visit = [(start_node, None, 0)]  # queue

    while len(nodes_to_visit) > 0:  # iterative not recursive to avoid extreme recursion depth
        node = nodes_to_visit[0][0]
        prev_node = nodes_to_visit[0][1]
        levels_deep = nodes_to_visit[0][2]
        nodes_to_visit = nodes_to_visit[1:]

        # if node pair not linked by edge and existing distance, if any, is longer
        lock.acquire()
        if prev_node is not None:
            old_dist = get_adj_matrix_entry(adj_mat_global, start_node, node)
            prev_dist = get_adj_matrix_entry(adj_mat_global, start_node, prev_node)
            if old_dist == 0 or old_dist > prev_dist + 1:
                set_adj_matrix_entry(adj_mat_global, start_node, node, prev_dist + 1)  # update distance
        lock.release()

        if levels_deep < depth_limit:
            for next_node in range(node_count):  # queue child nodes
                node_visited_status[node] = 2
                if node_visited_status[next_node] != 2 and get_adj_matrix_entry(adj_mat_global, node, next_node) == 1:
                    nodes_to_visit.append((next_node, node, levels_deep + 1))
                    if node_visited_status[next_node] == 0:
                        node_visited_status[node] = 1
    return None


def bfs_helper(entry, lock, depth_limit):
    """Helper method to iterate over each node in a process's chunk."""
    node_count = entry[0]
    start_node = entry[1]
    name = entry[2]
    shape = entry[3]
    dtype = entry[4]
    chunksize = entry[5]
    nodes_included = entry[6]
    print("Processing chunk from " + str(start_node) + " to " + str(start_node + chunksize - 1))  # logging
    for i in range(chunksize):
        bfs(start_node + i, node_count, name, shape, dtype, lock, depth_limit)
        print("Processed node " + str(start_node + i) + " of " + str(len(nodes_included)))  # logging
    return None


def bfs_all(adj_matrix, node_count, nodes_included):
    """Runs bfs() starting from each node in the graph iteratively."""
    print("Processing nodes...")
    lock = multiprocessing.Lock()
    procs = []
    adj_iter = AdjacencyIterator(adj_matrix, int(node_count / NTHREADS) + 1, node_count, nodes_included)
    for entry in adj_iter:
        proc = Process(target=bfs_helper, args=(entry, lock, DEPTH_LIMIT))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()

    # Based on example at
    # https://docs.python.org/3/library/multiprocessing.shared_memory.html#module-multiprocessing.shared_memory

    sharedmem = SharedMemory(name=adj_iter.sharedmem_name)
    adj_matrix_sh = numpy.ndarray(adj_iter.sharedmem_shape, dtype=adj_iter.sharedmem_dtype, buffer=sharedmem.buf)
    adj_matrix = numpy.ndarray(adj_iter.sharedmem_shape, dtype=adj_iter.sharedmem_dtype)
    adj_matrix[:] = adj_matrix_sh[:]

    print("Processed nodes...")
    sharedmem.unlink()
    sharedmem.close()
    return adj_matrix


def print_adjmatrix(adj_matrix, keys_list):
    """Prints the adjacency matrix to the console for debugging."""
    print("  ", end="")  # print a space so the header lines up

    for node in keys_list:  # print header
        print(str(node) + " ", end="")

    print("\n", end="")

    i = 0

    for row in adj_matrix:
        print(keys_list[i] + " ", end="")  # print "header" down left side
        for col in row:
            print(str(col) + " ", end="")  # print data
        print("\n", end="")
        i += 1


def output_distances(adj_matrix, filename, node_list):
    """Outputs the distances in CSV format."""
    with open(filename, "w") as outfile:
        rownum = 0
        for row in adj_matrix:
            colnum = 0
            for col in row:
                if rownum < colnum and col != 0:  # only output each distance once and only output nonzero distances
                    outfile.write(node_list[rownum] + "," + node_list[colnum] + "," + str(col) + "\n")
                colnum += 1
            rownum += 1


if __name__ == '__main__':  # to prevent each worker process from running this part

    adjlist_input = {}
    all_nodes = []

    with open(sys.argv[1]) as f:
        line_num = 0
        for line in f:
            if line_num % 10000 == 0:  # print log message every 10000 lines
                print("Reading line " + str(line_num))

            edge = line.split(",")  # process csv line

            if edge[0].strip() not in adjlist_input:  # if node not in adj list
                adjlist_input[edge[0].strip()] = [edge[1].strip()]  # add node
            else:
                adjlist_input[edge[0].strip()].append(edge[1].strip())  # add edge to node

            if edge[0].strip() not in all_nodes:  # add node to node list if not present
                all_nodes.append(edge[0].strip())
            if edge[1].strip() not in all_nodes:  # add node to node list if not present
                all_nodes.append(edge[1].strip())
            line_num += 1

    included_node_names = []  # the list of nodes to include in the analysis

    with open(sys.argv[2]) as nodes_file:  # read in the list of nodes to use
        for line in nodes_file:
            included_node_names.append(line.strip())

    node_index_map = map_nodes_to_indices(
        included_node_names)  # mapping node names to numeric indices for creation of adjacency matrix

    nnodes = len(node_index_map.keys())  # number of nodes

    included_nodes_list = list(node_index_map.keys())  # list of node names

    adjmatrix_input = adj_list_to_matrix(adjlist_input, node_index_map,
                                         included_node_names)  # generate adjacency matrix

    adjmatrix_input = bfs_all(adjmatrix_input, nnodes, included_nodes_list)  # run the actual analysis

    output_distances(adjmatrix_input,
                     sys.argv[1].replace(".csv", "." + sys.argv[3] + ".deep_pdistances.csv").replace("samples/",
                                                                                                     "distances/"),
                     included_nodes_list)  # output distances to file

    # print_adjmatrix(adjmatrix_input, included_nodes) # print matrix for debug
