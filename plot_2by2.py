import sys
import matplotlib.pyplot as plt

# Read in data from 4 files (for 2x2 plot)

p1_x = []
p1_y = []

with open(sys.argv[1]) as f:
	for line in f:
		l = line.split(",")
		p1_x.append(float(l[0]))
		p1_y.append(float(l[1]))


p2_x = []
p2_y = []

with open(sys.argv[2]) as f:
	for line in f:
		l = line.split(",")
		p2_x.append(float(l[0]))
		p2_y.append(float(l[1]))


p3_x = []
p3_y = []

with open(sys.argv[3]) as f:
	for line in f:
		l = line.split(",")
		p3_x.append(float(l[0]))
		p3_y.append(float(l[1]))


p4_x = []
p4_y = []

with open(sys.argv[4]) as f:
	for line in f:
		l = line.split(",")
		p4_x.append(float(l[0]))
		p4_y.append(float(l[1]))


# Data for plot (hardcoded because this is for one special purpose)

x = [p1_x, p2_x, p3_x, p4_x]
y = [p1_y, p2_y, p3_y, p4_y]
titles = ["Semantic Links 1000-10000", "Semantic Links 1000-20000", "Etymological Links 1000-10000", "Etymological Links 1000-20000"]
colors = ["tab:blue", "tab:blue", "tab:orange", "tab:orange"]


# Plot the data

fig, axes = plt.subplots(2, 2)

i=0
for axis in axes.flat: # plot the 4 graphs
	axis.set_title(titles[i])
	axis.plot(x[i], y[i], color=colors[i])
	axis.set_xlabel("Sample Size (words)")
	axis.set_ylabel("Average Edge Count")
	i+=1

plt.show()