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


names = ["2500 All Etym", "1000 All Etym", "2500 No Roots", "1000 No Roots/Affixes", "1000 Only Roots",
            "1000 No Affixes", "1000 No Roots", "2500 No Roots/Affixes", "2500 No Affixes"]

colors = ["tab:blue", "tab:orange", "tab:green", "tab:purple", "tab:red", "tab:brown", "tab:pink", "tab:gray", "tab:olive"]

markers = [".", "^", "s", "+", "d", "x", "*", "D", "p"]

ind = 0

plots = []

for sample in names:
    # plot samples
    plots.append(plt.scatter(data_x[(ind*80):(ind*80)+80], data_y[(ind*80):(ind*80)+80], c=colors[ind], s=10, marker=markers[ind]))
    ind+=1

plt.legend(plots, names)  # legend
plt.show()  # show graph
