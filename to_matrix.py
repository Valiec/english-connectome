import sys

nodes_set = set()

edges_sem = []

edges_etym = []

with open(sys.argv[1]) as f:
	for line in f:
		line_split = line.split(",")
		line_split[0] = line_split[0].strip()
		line_split[1] = line_split[1].strip()
		edges_sem.append(line_split)
		nodes_set.add(line_split[0])
		nodes_set.add(line_split[1])

with open(sys.argv[2]) as f:
	for line in f:
		line_split = line.split(",")
		line_split[0] = line_split[0].strip()
		line_split[1] = line_split[1].strip()
		edges_etym.append(line_split)
		nodes_set.add(line_split[0])
		nodes_set.add(line_split[1])


nodes = list(nodes_set)

node_lookup = {}

i = 0
for node in nodes:
	node_lookup[node] = i
	i+=1

mat_sem = []

mat_etym = []

for i in range(len(nodes)):
	row_sem = []
	row_etym = []
	for j in range(len(nodes)):
		row_sem.append(0)
		row_etym.append(0)
	mat_sem.append(row_sem)
	mat_etym.append(row_etym)


for edge in edges_sem:
	row = node_lookup[edge[0]]
	col = node_lookup[edge[1]]
	val = float(edge[2])
	mat_sem[row][col] = val
	mat_sem[col][row] = val

for edge in edges_etym:
	row = node_lookup[edge[0]]
	col = node_lookup[edge[1]]
	val = float(edge[2])
	mat_etym[row][col] = val
	mat_etym[col][row] = val

with open(sys.argv[1].replace(".csv", "_mat.csv").replace("distances/", "matrices/"), "w") as f:
	for row in mat_sem:
		line = ""
		for col in row:
			line=line+(str(col))+","
		line = line[:-1]+"\n"
		f.write(line)

with open(sys.argv[2].replace(".csv", "_mat.csv").replace("distances/", "matrices/"), "w") as f:
	for row in mat_etym:
		line = ""
		for col in row:
			line=line+(str(col))+","
		line = line[:-1]+"\n"
		f.write(line)