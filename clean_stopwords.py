import sys

stop_words = []

with open("stopwords-en.txt") as f:
    for line_raw in f:
        stop_words.append(line_raw.strip())

i = 0

with open(sys.argv[1]) as f:
    with open(sys.argv[2], "w") as g:
        for line_raw in f:
            stopword_found = False
            if i % 10000 == 0:
                print("Processing line " + str(i) + "...")
            line = line_raw.split(",")
            for word in stop_words:
                if word in line:
                    stopword_found = True
            if not stopword_found:
                g.write(line_raw)
            i += 1
