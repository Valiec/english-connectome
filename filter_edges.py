# Filters a set of edges to only include those between nodes in a set of nodes

# Usage: python filter_edges.py <edge list> <node list>

import sys

edges = []

nodes = set()


with open(sys.argv[1]) as f:
	for line in f:
		line_split = line.strip().split(",")
		edges.append([line_split[0].strip(), line_split[1].strip()])

with open(sys.argv[2]) as f:
	for line in f:
		nodes.add(line.strip())


for edge in edges:
	if edge[0] in nodes and edge[1] in nodes:
		print(edge[0]+","+edge[1])

