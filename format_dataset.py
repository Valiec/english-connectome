import os
import sys
from wiktionary_reader import *

words_data = {}
words_data_raw = {}
plurals_map = {}
synonyms_map = {}
alt_spellings_map = {}
forms_map = {}

base_path = sys.argv[1]

dirs = os.listdir(base_path)
dirs.sort()

for words_dir in dirs:
    if os.path.isdir(base_path + "/" + words_dir):
        # if words_dir != "S" and words_dir != "s":
        #     continue
        print("Processing directory "+words_dir+" ", end="")
        files = os.listdir(base_path + "/" + words_dir)
        print("("+str(len(files))+" files)")
        for file in files:
            if file.endswith(".json"):
                parse_file(base_path + "/" + words_dir + "/" + file, plurals_map, synonyms_map, forms_map,
                           alt_spellings_map, words_data, words_data_raw)


with open("word_data_out.txt", "wb") as f:
    for word in words_data.keys():
        f.write((word + "\t" + (words_data[word]) + "\n").encode('utf8'))

with open("word_data_out_raw.txt", "wb") as f:
    for word in words_data.keys():
        f.write((word + "\t" + (words_data_raw[word]) + "\n").encode('utf8'))

with open("plurals_out.txt", "wb") as f:
    for word in plurals_map.keys():
        f.write((word + "\t" + (plurals_map[word]) + "\n").encode('utf8'))

with open("synonyms_out.txt", "wb") as f:
    for word in synonyms_map.keys():
        f.write((word + "\t" + (synonyms_map[word]) + "\n").encode('utf8'))

with open("alt_spellings_out.txt", "wb") as f:
    for word in alt_spellings_map.keys():
        f.write((word + "\t" + (alt_spellings_map[word]) + "\n").encode('utf8'))

with open("forms_out.txt", "wb") as f:
    for word in forms_map.keys():
        f.write((word + "\t" + (forms_map[word]) + "\n").encode('utf8'))
