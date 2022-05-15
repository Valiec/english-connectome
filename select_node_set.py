# Gets a list of edges within a given depth of a starting node, downsampled to a given fraction (but a given number of times more likely if directly connected to the starting node)

# Usage python select_node_set.py <edge list> <start node> <depth> <downsampling factor> <direct connection multiplier> [node filter]

import sys
import random

adjlist_input = {}

edge_list = []

node_set = set()


def stderr_log(text):
    """Convenience function for me to log to stderr without forgetting the newline."""
    sys.stderr.write(text + "\n")


with open(sys.argv[1]) as f:  # read in file
    line_num = 0
    for line in f:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        edge = line.split(",")
        edge_list.append(edge)
        reverse_edge = [edge[1], edge[0]]  # undirected graph
        edge_list.append(reverse_edge)

        if edge[0].strip() not in adjlist_input:  # add edge
            adjlist_input[edge[0].strip()] = [edge[1].strip()]
        else:
            adjlist_input[edge[0].strip()].append(edge[1].strip())

        if edge[1].strip() not in adjlist_input:  # undirected graph
            adjlist_input[edge[1].strip()] = [edge[0].strip()]
        else:
            adjlist_input[edge[1].strip()].append(edge[0].strip())

        if edge[0].strip() not in node_set:
            node_set.add(edge[0].strip())
        if edge[1].strip() not in node_set:
            node_set.add(edge[1].strip())
        line_num += 1

start_node = sys.argv[2]  # node to start at

if start_node.strip() not in node_set:  # start node invalid or nonexistent
    stderr_log("Cannot find start node!")
    for entry in node_set:
        print(entry, entry == start_node)
    sys.exit(-1)

radius = int(sys.argv[3])  # max distance away from the central node

node_filter = None

chance = float(sys.argv[4])  # fraction of nodes to retain when downsampling


prob_multiplier = int(sys.argv[5])  # the amount to multiply chance by for nodes directly connected to the starting node

if len(sys.argv) >= 7:  # optional filter file to restrict nodes
    node_filter = set()
    with open(sys.argv[6]) as f:
        for line in f:
            if line.strip() not in node_filter:
                node_filter.add(line.strip())

nodes_prelim = set()

nodes = set()

nodes_directly_connected = set()

nodes_to_test = [start_node]

i = 0

visited_edges = set()

while i < radius:  # loop over nodes and select nodes within radius of starting node
    nodes_to_test_next = []
    for node in nodes_to_test:
        if node in adjlist_input:  # if node has edges recorded
            potential_next_nodes = adjlist_input[node]
            for next_node in potential_next_nodes:
                if node <= next_node:
                    if node+","+next_node in visited_edges:
                        continue
                    visited_edges.add(node+","+next_node)
                else:
                    if next_node+","+node in visited_edges:
                        continue
                    visited_edges.add(next_node+","+node)
                if next_node != "type" and next_node != "characteristic":
                    nodes_to_test_next.append(next_node)  # add children to list of nodes to visit
                if node == start_node:
                    nodes_directly_connected.add(next_node)
            nodes_prelim.add(node)
    nodes_to_test = nodes_to_test_next
    i += 1

for node in nodes_prelim:
    if node_filter is None or node in node_filter:  # only select nodes passing filter
        if (random.random() < chance) or (random.random() < chance*prob_multiplier and node in nodes_directly_connected) or node.strip() == "fiction" or node.strip() == "dough" or node.strip() == "phyllo" or node.strip() == "type":  # downsampling
            nodes.add(node)

printed_edges = set()

for edge in edge_list:  # output edges
    if (edge[0].strip() in nodes) and (edge[1].strip() in nodes):  # if edge includes only nodes in sample
        edge_test = edge
        if edge[0].strip() > edge[1].strip():
            edge_test = [edge[1], edge[0]]
        printed_edges.add(edge_test[0]+","+edge_test[1])
        if (edge[0]+","+edge[1]) not in printed_edges:  # prevent duplication
            print(edge[0].strip() + ", " + edge[1].strip())
