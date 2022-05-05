import sys

mantel = []

with open(sys.argv[1]) as f:
	for line in f:
		if line.startswith("sample,"):
			continue  # skip header
		line_split = line.split(",")
		line_split[0] = line_split[0].strip()
		line_split[1] = float(line_split[1].strip())
		line_split[2] = float(line_split[2].strip())
		mantel.append(line_split)


means = []

counts = []


for i in range(int(len(mantel)/80)):
	means.append(0)
	counts.append(0)


ind = 0
i = 0
for line in mantel:
	means[ind]+=line[1]
	if line[1] < 0.05:
		counts[ind]+=1
	i+=1
	if i == 80:
		i=0
		ind+=1

i = 0
for val in means:
	means[i] = means[i]/80.0
	i+=1

print("set,mean,count")

for i in range(len(means)):
	print("set_"+str(i+1)+","+str(means[i])+","+str(counts[i]))
