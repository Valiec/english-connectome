import sys
import random
import matplotlib.pyplot as plt

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
        nodes_list[edge[0]] = 0
        nodes_list[edge[1]] = 0
        line_num+=1
    return list(nodes_list.keys())

def filter_edges_count(all_edges, nodes):
    """Filters out all edges not between nodes in nodes, and returns the count of such edges."""
    filtered_edges = 0
    for edge in all_edges:
        if (edge[0].strip() in nodes) and (edge[1].strip() in nodes):
            filtered_edges+=1
    return filtered_edges

def filter_edges(all_edges, nodes):
    """Filters out all edges not between nodes in nodes, and returns the list of such edges."""
    filtered_edges = []
    for edge in all_edges:
        if (edge[0].strip() in nodes) and (edge[1].strip() in nodes):
            filtered_edges.append(edge)
    return filtered_edges

edge_list = []

node_list = []

with open(sys.argv[1]) as f: # reading in edge list
    line_num = 0
    for line in f:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        edge = line.split(",")
        edge_list.append(edge)
        line_num += 1

stderr_log("Reading node list...")
node_list = []
with open(sys.argv[2]) as g: # reading in node list
    line_num = 0
    for line in g:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        node_list.append(line.strip())
        line_num += 1
stderr_log(str(len(node_list))+" nodes found.")


sizes = []
size_ratios = []

REP_COUNT = 10 # constant

for size in range(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])):
    stderr_log("Processing "+str(size)) 
    nodes_sample = random.sample(node_list, size) # get node sample
    new_edges = 0
    for i in range(REP_COUNT): # run REP_COUNT replicates of edge counting
        new_edges += filter_edges_count(edge_list, set(nodes_sample))
    new_edges = new_edges/float(REP_COUNT)
    new_edge_list = filter_edges(edge_list, set(nodes_sample))

    with open(sys.argv[1].replace(".csv", "_sample_").replace("data/", "samples/")+str(size)+".csv", "w") as f: # output sample
        for edge in new_edge_list:
            f.write(edge[0].strip()+","+edge[1].strip()+"\n")

    print(str(size)+", "+str(new_edges)+", "+str(new_edges/float(size))) # output average edge count and edge-to-node ratio

    sizes.append(new_edges)
    size_ratios.append(new_edges/float(size))

if sys.argv[8] == "ratio": # flag to specify edge-to-node ratio vs edge count
    axes = plt.axes()
    plt.title("Edges-to-Sample-Size ratio vs. Sample Size for "+sys.argv[6])
    axes.set_xlabel("Sample Size (words)")
    axes.set_ylabel("Average Edge Count")
    plt.plot(range(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])), size_ratios) # plot data
    plt.savefig("edge_ratios_"+sys.argv[7]+".svg", format="svg")
    plt.savefig("edge_ratios_"+sys.argv[7]+".png", format="png")
elif sys.argv[8] == "count": # flag to specify edge-to-node ratio vs edge count
    axes = plt.axes()
    plt.title("Edges vs. Sample Size for "+sys.argv[6])
    axes.set_xlabel("Sample Size (words)")
    axes.set_ylabel("Average Edge Count")
    plt.plot(range(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])), sizes) #plot data
    plt.savefig("edges_"+sys.argv[7]+".svg", format="svg")
    plt.savefig("edges_"+sys.argv[7]+".png", format="png")
else:
    pass