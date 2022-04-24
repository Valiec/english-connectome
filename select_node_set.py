import sys
import random

adjlist_input = {}

edge_list = []

node_set = set()

def stderr_log(text):
    """Convenience function for me to log to stderr without forgetting the newline."""
    sys.stderr.write(text+"\n")

with open(sys.argv[1]) as f:  # read in file
    line_num = 0
    for line in f:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        edge = line.split(",")
        edge_list.append(edge)
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

filter = None

chance = float(sys.argv[4])  # fraction of nodes to retain when downsampling

if len(sys.argv) >= 6:  # optional filter file to restrict nodes
    filter = set()
    with open(sys.argv[5]) as f:
        for line in f:
            if line.strip() not in filter:
                filter.add(line.strip())

nodes = set()

nodes_to_test = [start_node]

i = 0

while i < radius:  #loop over nodes and select nodes within radius of starting node
    nodes_to_test_next = []
    for node in nodes_to_test:
        if filter == None or node in filter:  # only select nodes passing filter
            if node in adjlist_input:  # if node has edges recorded
                nodes_to_test_next.extend(adjlist_input[node])  # add children to list of nodes to visit
                if random.random() < chance:  # downsampling
                    nodes.add(node)
    nodes_to_test = nodes_to_test_next
    i+=1

for edge in edge_list:  # output edges
    if (edge[0].strip() in nodes) and (edge[1].strip() in nodes):  # if edge includes only nodes in sample
        print(edge[0].strip()+", "+edge[1].strip())
