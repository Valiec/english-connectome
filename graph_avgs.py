import sys
import matplotlib.pyplot as plt


def stderr_log(text):
    """Convenience function for me to log to stderr without forgetting the newline."""
    sys.stderr.write(text + "\n")


data_x = []
data_y = []

with open(sys.argv[1]) as f:  # read in averages CSV
    for line in f:
        if line.startswith("sample,"):  # header
            continue
        line_split = line.split(",")
        data_x.append(float(line_split[1]))
        data_y.append(float(line_split[2]))

# setup plot
axes = plt.axes()
plt.title("Semantic vs. Etymological Distances")
axes.set_xlabel("Average Semantic Distances (edges)")
axes.set_ylabel("Average Etymological Distance (edges)")

# plot samples
p1 = plt.scatter(data_x[0:80], data_y[0:80], c="tab:blue", s=10)
p2 = plt.scatter(data_x[80:160], data_y[80:160], c="tab:orange", s=10, marker="^")
p3 = plt.scatter(data_x[160:240], data_y[160:240], c="tab:green", s=10, marker="s")
p4 = plt.scatter(data_x[240:320], data_y[240:320], c="tab:purple", s=10, marker="+")
p5 = plt.scatter(data_x[320:400], data_y[320:400], c="tab:red", s=10, marker="d")
p6 = plt.scatter(data_x[400:480], data_y[400:480], c="tab:brown", s=10, marker="x")
p7 = plt.scatter(data_x[480:560], data_y[480:560], c="tab:pink", s=10, marker="*")

plt.legend([p1, p2, p3, p4, p5, p6, p7],
           ["2500 All Etym", "1000 All Etym", "2500 No Roots", "1000 No Roots/Affixes", "1000 Only Roots",
            "1000 No Affixes", "1000 No Roots"])  # legend
plt.show()  # show graph
