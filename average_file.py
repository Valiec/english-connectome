import sys

# read in files
f = open(sys.argv[1])
g = open(sys.argv[2])

# init averages
average_f = 0.0
average_g = 0.0

# init counts
f_count = 0
g_count = 0

# get average distance from file 1
for line in f:
	line_split = line.split(",")
	average_f += float(line_split[2])
	f_count += 1

average_f = average_f / float(f_count)

# get average distance from file 2
for line in g:
	line_split = line.split(",")
	average_g += float(line_split[2])
	g_count += 1

average_g = average_g / float(g_count)

# get sample name
name = ("sample_" + (((sys.argv[1]).split("_")[2]).split(".")[0]))

# output line
print(name + "," + str(average_f) + "," + str(average_g))

# close files
f.close()
g.close()
