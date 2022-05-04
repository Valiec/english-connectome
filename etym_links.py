# Calculates the etymological connectome

# Usage python etym_links.py <input file> [output name]

import sys

term_ids = {}  # map of term IDs to terms

group_lines = []  # lines with "group_affix_root", "group_related_root", or "group_derived_root"

half_links = {}  # eng -> non-eng links
half_links_reverse = {}  # non-eng -> eng links
eng_keys = set()  # english term IDs

stopwords = []  # stop words

type_exclusions = set()

exclusions_method = "exclude"
# "include" accepts only lines with types in type_exclusions, "exclude" accepts only lines with types that are not

if len(sys.argv) > 4:
    exclusions_method = sys.argv[3]
    for entry in sys.argv[4:]:
        type_exclusions.add(entry)

with open("stopwords-en.txt") as f:  # read stop words
    for line in f:
        stopwords.append(line.strip().lower())

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

        if line[3] == "group_affix_root" or line[3] == "group_related_root" or \
                line[3] == "group_derived_root":  # skip group lines
            group_lines.append(line)
            continue

        if line[3] in type_exclusions and exclusions_method == "exclude":  # skip all lines of types in type_exclusions
            sys.stderr.write("Skipping line '" + line_raw.strip() + "' with excluded type " + line[3].strip() + "\n")
            continue

        if line[3] not in type_exclusions \
                and exclusions_method == "include":
            # skip all lines of types not in type_exclusions
            sys.stderr.write("Skipping line '" + line_raw.strip() + "' with excluded type " + line[3].strip() + "\n")
            continue

        if line[2].strip() == "" or line[6].strip() == "":  # blank entry
            sys.stderr.write("Skipping line '" + line_raw.strip() + "' with missing data\n")
            continue

        if line[1] == "English" and line[2].strip().lower() in stopwords:
            # sys.stderr.write("Skipping line '" + line_raw.strip() + "' with stop word "+line[2].strip().lower()+"\n")
            # logging deactivated as it is excessive
            continue

        if line[5] == "English" and line[6].strip().lower() in stopwords:
            # sys.stderr.write("Skipping line '" + line_raw.strip() + "' with stop word "+line[6].strip().lower()+"\n")
            # logging deactivated as it is excessive
            continue

        elif line[5] != "English" and line[1] == "English":
            if line[4] not in half_links_reverse.keys():  # add term ID for non-english word to half_links_reverse
                half_links_reverse[line[4]] = []
            if line[0] not in half_links.keys():  # add term ID for english word to half_links
                half_links[line[0]] = []
            half_links_reverse[line[4]].append([line[0], line[1], line[3], True])  # reverse
            half_links[line[0]].append([line[4], line[1], line[3], True])  # forward
            eng_keys.add(line[0])  # list english term ID in eng_keys
        else:
            pass
        i = i + 1
print(len(eng_keys))  # logging

key_lines = []

i = -1

name_prefix = ""

if sys.argv[2] != "-":  # using - as placeholder for "no prefix"
    name_prefix = "_" + sys.argv[2]

with open("data/etym_links" + name_prefix + ".csv", "w") as f:
    for key in eng_keys:
        i += 1
        if i % 10 == 0:  # log every 10 lines output
            print("Processing line " + str(i) + "...")
        if key not in half_links:  # if word has no links, skip
            continue
        entries_for_foreign_word = {}
        entries_for_eng_word = {}
        foreign_words = []
        # print("key is: "+str(term_ids[key]))
        entry = "BAD"  # placeholder value to catch errors
        for entry in half_links[key]:  # loop over links from word
            foreign_words.append(entry[0])  # add to foreign words list
            entries_for_foreign_word[entry[0]] = entry  # store mapping of foreign words to link entries
        for word in foreign_words:  # iterate over foreign words
            if word not in half_links_reverse:  # if no link to an english word from here, skip
                continue
            eng_words = []
            entry_2 = "BAD"  # placeholder value to catch errors
            for entry_2 in half_links_reverse[word]:  # loop over links from foreign word
                eng_words.append(entry_2[0])
                entries_for_eng_word[entry_2[0]] = entry_2  # store mapping of english words to link entries
            for eng_word in eng_words:  # loop over english words
                if eng_word != key:  # do not store links of words to themselves
                    # get actual entries for words, not term IDs
                    entry = entries_for_foreign_word[word]
                    entry_2 = entries_for_eng_word[eng_word]

                    # output link
                    f.write(term_ids[key][1] + "," + term_ids[eng_word][1] + "," + term_ids[entry[0]][0] + "," +
                            term_ids[entry[0]][1] + "," + entry[2] + "," + entry_2[2] + "\n")
