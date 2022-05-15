# Splits single Mantel output file into batches for each set of 80 samples for median and MAD calculation.

# Usage: python split_mantel.py <data CSV>

import sys

mantel = []

with open(sys.argv[1]) as f:
	for line in f:
		if line.startswith("sample,"):
			continue  # skip header
		mantel.append(line.strip())


lines = []

counts = []


for i in range(int(len(mantel)/80)):
	lines.append([])


ind = 0
i = 0
for line in mantel:
	lines[ind].append(line.strip())
	i+=1
	if i == 80:
		i=0
		ind+=1


ind = 0
for batch in lines:
	with open("data/mantel_data_"+str(ind+1)+".csv", "w") as f:
		f.write("sample,signif,r\n")
		for i in range(len(batch)):
			f.write(batch[i]+"\n")
	ind+=1
