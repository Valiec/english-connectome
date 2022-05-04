# library for sem_links.py


from clean_data import *


def load_entries(words_filename, headwords_data):
    """loads definitions from data file

    definitions are in one file, where a word and its definition are on one line,
    with the first word in the line being the headword"""
    wordlist_raw = {}
    # loads in the words and definitions
    with open(words_filename) as f:
        for line in f:
            headword = line.split("\t")[0]
            definition = " ".join((line.split("\t")[1]).split(" ")[1:])
            wordlist_raw[headword] = definition
            headwords_data.append(headword)
    return wordlist_raw


def load_exclusions(exclusions_filename, headwords):
    """loads exclusions from data file

    exclusions are listed one per line"""
    exclusions = []
    with open(exclusions_filename) as f:
        for line in f:
            exclusions.append(clean_word(line, headwords))
    return exclusions
