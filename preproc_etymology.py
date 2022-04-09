import sys

term_ids = {}

group_lines = []

links = {}
half_links = {}
half_links_reverse = {}
eng_keys = set()
i = -1
with open(sys.argv[1]) as f:
    for line_raw in f:
        line = line_raw.split(",")
        if len(line) < 11:  # truncated
            sys.stderr.write("Skipping truncated line '" + line_raw.strip() + "'\n")
            continue
        if line[1] != "English" and line[5] != "English":  # link does not involve English
            continue
        if i % 100 == 0:
            print("processing line " + str(i) + "...")
        # print(line)

        if line[0].strip() not in term_ids.keys():
            term_ids[line[0].strip()] = [line[1], line[2]]

        if line[4].strip() not in term_ids.keys():
            term_ids[line[4].strip()] = [line[5], line[6]]

        if line[3] == "group_affix_root" or line[3] == "group_related_root" or line[3] == "group_derived_root":
            group_lines.append(line)
            continue

        if line[2].strip() == "" or line[6].strip() == "":  # blank entry
            sys.stderr.write("Skipping line '" + line_raw.strip() + "' with missing data\n")
            continue

        if line[1] != "English" and line[5] == "English" and False:
            if line[0] not in half_links_reverse.keys():
                half_links_reverse[line[0]] = []
            # half_links[line[0]].append([line[6], line[5], line[3], False])  # forward
            if line[4] not in half_links.keys():
                half_links[line[4]] = []
            half_links_reverse[line[0]].append([line[4], line[5], line[3], False])  # forward
            half_links[line[4]].append([line[0], line[5], line[3], True])  # reverse
            eng_keys.add(line[4])
            # half_links_reverse[line[6]].append([line[2], line[5], line[3], False])  # forward
        elif line[5] != "English" and line[1] == "English":
            if line[4] not in half_links_reverse.keys():
                half_links_reverse[line[4]] = []
            if line[0] not in half_links.keys():
                half_links[line[0]] = []
            half_links_reverse[line[4]].append([line[0], line[1], line[3], True])  # reverse
            half_links[line[0]].append([line[4], line[1], line[3], True])  # forward
            eng_keys.add(line[0])
        else:
            if line[2] not in links.keys():
                links[line[2]] = []
            links[line[2]].append(line[6])
        i = i + 1
print(len(eng_keys))

key_lines = []

i = -1

with open("etym_links_out.csv", "w") as f:
    for key in eng_keys:
        i += 1
        if i % 10 == 0:
            print("processing line " + str(i) + "...")
        if key not in half_links:
            continue
        entries_for_word_debug_1 = {}
        entries_for_word_debug_2 = {}
        foreign_words = []
        # print("key is: "+str(term_ids[key]))
        entry = "BAD"
        for entry in half_links[key]:
            foreign_words.append(entry[0])
            entries_for_word_debug_1[entry[0]] = entry
        for word in foreign_words:
            if word not in half_links_reverse:
                continue
            eng_words = []
            entry_2 = "BAD"
            for entry_2 in half_links_reverse[word]:
                eng_words.append(entry_2[0])
                entries_for_word_debug_2[entry_2[0]] = entry_2
            for eng_word in eng_words:
                if eng_word != key:
                    # pass
                    entry = entries_for_word_debug_1[word]
                    entry_2 = entries_for_word_debug_2[eng_word]
                    f.write(term_ids[key][1] + "," + term_ids[eng_word][1] + "," + term_ids[entry[0]][0] + "," +
                            term_ids[entry[0]][1] + "," + entry[2] + "," + entry_2[2] + "\n")

# with open("etym_links_out.csv", "w") as f:
#    #for word in half_links.keys():  # debug code to output all raw links
#    #    for dest_word in half_links[word]:
#    #        f.write(word+","+dest_word[0]+"\n")
#    for line in key_lines:
#        f.write(line)
