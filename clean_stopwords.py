# Removes stopwords from a graph

# Usage python clean_stopwords.py <input file> <output file>

import sys

stop_words = set()

with open("stopwords-en.txt") as f:  # load stop words
    for line_raw in f:
        if line_raw.strip() not in stop_words:
            stop_words.add(line_raw.strip())

i = 0

with open(sys.argv[1]) as f:  # load edge list
    with open(sys.argv[2], "w") as g:  # open output file
        for line_raw in f:  # loop over edges
            stopword_found = False
            if i % 10000 == 0:  # logging
                print("Processing line " + str(i) + "...")
            line = line_raw.split(",")
            line[0] = line[0].strip()
            line[1] = line[1].strip()
            for word in stop_words:
                if word in line:  # check if either word is a stopword
                    stopword_found = True
            if not stopword_found:  # write out line if no stop word
                g.write(line_raw)
            i += 1
