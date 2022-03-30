import networkx as nx
import sys
import matplotlib.pyplot as plt

stop_words = []

with open("stopwords-en.txt") as f:
	for line in f:
		stop_words.append(line.strip())

the_graph = nx.Graph()

with open(sys.argv[1]) as f:
	for line in f:
		l = line.split(",")
		if l[0].strip().lower() in stop_words or l[1].strip().lower() in stop_words:
			continue
		the_graph.add_edge("\""+l[0].strip()+"\"", "\""+l[1].strip()+"\"")


#print(the_graph.number_of_edges())

with open(sys.argv[1]) as f:
	for line in f:
		l = line.split(",")
		if l[0].strip().lower() in stop_words or l[1].strip().lower() in stop_words:
			continue
		n1 = "\""+l[0].strip()+"\""
		n2 = "\""+l[1].strip()+"\""

		if the_graph.degree(n1) == 1 and the_graph.degree(n2) == 1:
			the_graph.remove_node(n1)
			the_graph.remove_node(n2)


d = the_graph.degree()

for l in d:
	print(l[0]+","+str(l[1]))

#nx.draw(the_graph, with_labels=False, font_weight='bold', node_size=10, font_size=5)
#nx.drawing.nx_pydot.write_dot(the_graph, "graphdata_nostop_real_prune.dot")
#nx.to_pydot(the_graph)
#plt.savefig("testfig.png")