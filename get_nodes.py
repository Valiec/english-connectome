import sys
import random

def stderr_log(text):
    """Convenience function for me to log to stderr without forgetting the newline."""
    sys.stderr.write(text+"\n")

def get_nodelist(edge_list):
    """Gets a list of all nodes in the graph represented by a given adjacency list."""
    nodes_list = set()
    line_num = 0
    edge_count = len(edge_list)
    for edge in edge_list:
        if line_num % 10000 == 0:
            stderr_log("Processing edge " + str(line_num)+" of "+str(edge_count))
        nodes_list.add(edge[0])
        nodes_list.add(edge[1])
        line_num+=1
    return list(nodes_list)

def filter_edges_count(all_edges, nodes):
    """Filters out all edges not between nodes in nodes, and returns the count of such edges."""
    filtered_edges = 0
    for edge in all_edges:
        if (edge[0].strip() in nodes) and (edge[1].strip() in nodes):
            filtered_edges+=1
    return filtered_edges

# init lists
edge_list = []
node_list = []

with open(sys.argv[1]) as f: # read in edges
    line_num = 0
    for line in f:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        edge = line.split(",")
        edge_list.append(edge)
        line_num += 1

stderr_log("Getting node list...")
node_list = get_nodelist(edge_list) # get node list
stderr_log(str(len(node_list))+" nodes found.")

with open(sys.argv[1].replace(".csv", "_nodes.txt"), "w") as f: # write out nodes
    for node in node_list:
        f.write(node+"\n")