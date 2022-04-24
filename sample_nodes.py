import sys
import random

def stderr_log(text):
    """Convenience function for me to log to stderr without forgetting the newline."""
    sys.stderr.write(text+"\n")

def get_nodelist(edge_list):
    """Gets a list of all nodes in the graph represented by a given adjacency list."""
    nodes_list = {}
    line_num = 0
    edge_count = len(edge_list)
    for edge in edge_list:
        if line_num % 10000 == 0:
            stderr_log("Processing edge " + str(line_num)+" of "+str(edge_count))
        nodes_list[edge[0].strip()] = 0
        nodes_list[edge[1].strip()] = 0
        line_num+=1
    return list(nodes_list.keys())

def filter_edges_count(all_edges, nodes):
    """Filters out all edges not between nodes in nodes, and returns the count of such edges."""
    filtered_edges = 0
    for edge in all_edges:
        if (edge[0].strip() in nodes) and (edge[1].strip() in nodes):
            filtered_edges+=1
    return filtered_edges


# init edge and node lists
edge_list_1 = []
edge_list_2 = []
node_list = []


with open(sys.argv[1]) as f: # reading in node list
    line_num = 0
    for line in f:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        node = line.strip()
        node_list.append(node)
        line_num += 1

with open(sys.argv[2]) as f: # reading in edge list for file 1
    line_num = 0
    for line in f:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        edge = line.split(",")
        edge_list_1.append(edge)
        line_num += 1

with open(sys.argv[3]) as f: # reading in edge list for file 2
    line_num = 0
    for line in f:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        edge = line.split(",")
        edge_list_2.append(edge)
        line_num += 1

offset = 0 # default starting sample number

if len(sys.argv) >= 10: # if starting sample number given, use that
    offset = int(sys.argv[9])

stderr_log(str(len(node_list))+" nodes found.")
for i in range(offset, int(sys.argv[4])+offset): # for all sample numbers to generate
    node_sample = random.sample(node_list, int(sys.argv[5])) # get node sample

    node_sample_set = set(node_sample) # turn this into a set for faster runtime

    with open("samples/"+sys.argv[6]+"_"+str(i+1)+".txt", "w") as f: # output node names for sample
        for node in node_sample:
            f.write(node.strip()+"\n")

    with open("samples/"+sys.argv[7]+"_"+str(i+1)+".csv", "w") as f: # output edges for file 1 sample
        for edge in edge_list_1:
            if edge[0].strip() in node_sample_set and edge[1].strip() in node_sample_set:
                f.write(edge[0].strip()+","+edge[1].strip()+"\n")

    with open("samples/"+sys.argv[8]+"_"+str(i+1)+".csv", "w") as f: # output node names for file 2 sample
        for edge in edge_list_2:
            if edge[0].strip() in node_sample_set and edge[1].strip() in node_sample_set:
                f.write(edge[0].strip()+","+edge[1].strip()+"\n")