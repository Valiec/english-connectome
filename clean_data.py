# library for sem_links.py

import re


def clean_word(raw_word, headwords):
    """cleans up extra punctuation and formatting from a word

    will strip newlines, spaces, tabs, and hyphens, and convert word to lowercase"""
    lower_word = raw_word.lower()
    regex = re.compile('[^a-z]')  # remove all non-alphabetic characters
    cleaned_word = regex.sub("", lower_word)

    if cleaned_word.endswith("s") and cleaned_word[:-1] in headwords:  # potential plural
        cleaned_word = cleaned_word[:-1]

    elif cleaned_word.endswith("ing") and cleaned_word[:-3] in headwords:  # potential participle or gerund
        cleaned_word = cleaned_word[:-3]

    elif cleaned_word.endswith("ed") and cleaned_word[:-2] in headwords:  # potential past tense verb
        cleaned_word = cleaned_word[:-2]
    else:
        pass

    # words ending in -er, -ly, or similar are going to have their own entries

    return cleaned_word


def clean_entries(word_data_raw, exclusions, headwords):
    """cleans out common and duplicate words"""
    # I could turn off deduplication if we want the duplication
    word_data = {}
    for headword in word_data_raw.keys():
        definition_str = word_data_raw[headword]
        definition_wordlist = definition_str.split()
        definition_cleaned_unique = []
        for word in definition_wordlist:
            word_clean = clean_word(word, headwords)  # clean word first to make sure exclusions don't mess up
            if word_clean in headwords and word_clean not in definition_cleaned_unique and word_clean not in exclusions:
                definition_cleaned_unique.append(word_clean)  # convert words to all-lowercase
        word_data[headword] = definition_cleaned_unique
    return word_data
