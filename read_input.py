from clean_data import *


# loads definitions from data file
# for testing, definitions are in one file, where a word and its definition are on one line,
# with the first word in the line being the headword
def load_entries(words_filename, headwords_data):
    wordlist_raw = {}
    # loads in the words and definitions
    with open(words_filename) as f:
        for line in f:
            headword = line.split("\t")[0]
            definition = " ".join((line.split("\t")[1]).split(" ")[1:])
            wordlist_raw[headword] = definition
            headwords_data.append(headword)
    return wordlist_raw


# loads exclusions from data file
# exclusions are listed one per line
def load_exclusions(exclusions_filename, headwords):
    exclusions = []
    with open(exclusions_filename) as f:
        for line in f:
            exclusions.append(clean_word(line, headwords))
    return exclusions
