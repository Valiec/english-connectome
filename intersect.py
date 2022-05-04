# Takes two sets of edges and returns the intersection

# Usage python intersect.py <file 1> <file 2>

import sys

node_list = {}


def stderr_log(text):
    """Convenience function for me to log to stderr without forgetting the newline."""
    sys.stderr.write(text + "\n")


with open(sys.argv[1]) as f:  # load in file 1
    line_num = 0
    for line in f:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        node_list[line.strip()] = 0  # set flag that this node has been seen in file 1
        line_num += 1

with open(sys.argv[2]) as g:  # load in file 2
    line_num = 0
    for line in g:
        if line_num % 10000 == 0:
            stderr_log("Reading line " + str(line_num))
        if line.strip() in node_list:
            node_list[line.strip()] = 1  # update flag to indicate it's been seen in both
        line_num += 1

with open(sys.argv[1].replace(".txt", "") + "_" + sys.argv[2].replace(".txt", "") + "_intersected.txt",
          "w") as h:  # output intersection
    for node in node_list.keys():
        if node_list[node] == 1:  # output only nodes seen in both files
            h.write(node + "\n")
