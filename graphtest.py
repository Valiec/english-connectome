import networkx as nx
import sys

stop_words = []

with open("stopwords-en.txt") as f:
	for line_raw in f:
		stop_words.append(line_raw.strip())

the_graph = nx.Graph()

with open(sys.argv[1]) as f:
	for line_raw in f:
		line = line_raw.split(",")
		if line[0].strip().lower() in stop_words or line[1].strip().lower() in stop_words:
			continue
		the_graph.add_edge("\""+line[0].strip()+"\"", "\""+line[1].strip()+"\"")


# print(the_graph.number_of_edges())

with open(sys.argv[1]) as f:
	for line_raw in f:
		line = line_raw.split(",")
		if line[0].strip().lower() in stop_words or line[1].strip().lower() in stop_words:
			continue
		n1 = "\""+line[0].strip()+"\""
		n2 = "\""+line[1].strip()+"\""

		if the_graph.degree(n1) == 1 and the_graph.degree(n2) == 1:
			the_graph.remove_node(n1)
			the_graph.remove_node(n2)


degree_list = the_graph.degree()

for node in degree_list:
	print(node[0]+","+str(node[1]))

# nx.draw(the_graph, with_labels=False, font_weight='bold', node_size=10, font_size=5)
# nx.drawing.nx_pydot.write_dot(the_graph, "graphdata_nostop_real_prune.dot")
# nx.to_pydot(the_graph)
# plt.savefig("testfig.png")
