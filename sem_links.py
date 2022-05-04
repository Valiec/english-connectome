# Calculates the semantic connectome

# Usage python sem_links.py <input file> [output name]

from read_input import *
from clean_data import *
from match_words import *
import sys

headwords_list = []
definitions_raw = load_entries(sys.argv[1], headwords_list)  # load definitions

# this currently only excludes articles for testing, but will handle all exclusions
exclusions_list = load_exclusions("stopwords-en.txt", headwords_list)

definitions_cleaned = clean_entries(definitions_raw, exclusions_list, headwords_list)  # clean definitions

semantic_links_raw = process_words(definitions_cleaned)  # find links

semantic_links = prune_self_links(semantic_links_raw)  # get rid of words linking to themselves

name_prefix = ""

if sys.argv[2] != "-":  # using - as placeholder for "no prefix"
    name_prefix = "_" + sys.argv[2]

with open("data/etym_links" + name_prefix + ".csv", "w") as f:
    for word in semantic_links.keys():  # debug code to output all raw links
        for dest_word in semantic_links[word]:
            f.write(word+","+dest_word+"\n")
