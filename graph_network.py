import networkx as nx
import sys

stop_words = []

with open("stopwords-en.txt") as f:  # read in stop words
    for line_raw in f:
        stop_words.append(line_raw.strip())

the_graph = nx.Graph()  # init graph

with open(sys.argv[1]) as f:  # read in edges
    lnum = 0
    for line_raw in f:
        if lnum % 100000 == 0:
            sys.stderr.write("Reading " + str(lnum) + "\n")
        line = line_raw.split(",")
        if line[0].strip().lower() in stop_words or line[1].strip().lower() in stop_words:  # filter stopwords again
            continue
        the_graph.add_edge("\"" + line[0].strip() + "\"", "\"" + line[1].strip() + "\"")  # add edges to graph
        lnum += 1

with open(sys.argv[1]) as f:  # read in edges again (for filtering)
    for line_raw in f:
        line = line_raw.split(",")
        if line[0].strip().lower() in stop_words or line[1].strip().lower() in stop_words:  # skip stopwords again
            continue
        n1 = "\"" + line[0].strip() + "\""  # get node names
        n2 = "\"" + line[1].strip() + "\""

        if the_graph.degree(n1) == 1 and the_graph.degree(n2) == 1:  # if this is an isolated pair of nodes
            the_graph.remove_node(n1)
            the_graph.remove_node(n2)

degree_list = the_graph.degree()
# get degrees of all nodes (if your IDE says calling degree() is invalid, it's wrong, ignore it)

for node in degree_list:  # output degree of each node
    print(node[0] + "," + str(node[1]))

nx.drawing.nx_pydot.write_dot(the_graph, "data/graphdata_" + sys.argv[1]
                              .replace(".csv", "").replace("data/", "") + ".dot")  # output dot file
