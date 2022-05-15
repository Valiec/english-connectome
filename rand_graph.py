# Generates a random graph with numbered nodes

# Usage: python3 rand_graph.py <output name> <node count>

import sys
import random

graph = {}

for i in range(int(sys.argv[2])):
	node1 = str(random.randint(1, int(sys.argv[2])))
	node2 = str(random.randint(1, int(sys.argv[2])))
	if node1 not in graph:
		graph[node1] = []
	graph[node1].append(node2)

with open(sys.argv[1], "w") as f:
		f.write("strict graph {\n")
		for node in graph.keys():
			for node2 in graph[node]:
				if node != node2:
					f.write("  \""+node+"\""+" -- "+"\""+node2+"\"\n")
		f.write("}\n")
