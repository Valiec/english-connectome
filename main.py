import re


# loads definitions from data file
# for testing, definitions are in one file, where a word and its definition are on one line,
# with the first word in the line being the headword
def load_entries(words_filename, headwords_data):
    wordlist_raw = {}
    # loads in the words and definitions
    with open(words_filename) as f:
        for line in f:
            headword = line.split(" ")[0]
            definition = " ".join(line.split(" ")[1:])
            wordlist_raw[headword] = definition
            headwords_data.append(headword)
    return wordlist_raw


# cleans up extra punctuation and formatting from a word
# will strip newlines, spaces, tabs, and hyphens, and convert word to lowercase
def clean_word(raw_word, headwords):
    lower_word = raw_word.lower()
    # TODO handle diacritics
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

    return cleaned_word


# cleans out common and duplicate words (I could turn off deduplication if we want the duplication)
def clean_entries(word_data_raw, exclusions, headwords):
    word_data = {}
    for headword in word_data_raw.keys():
        definition_str = word_data_raw[headword]
        definition_wordlist = definition_str.split()
        definition_cleaned_unique = []
        for word in definition_wordlist:
            word_clean = clean_word(word, headwords)  # clean word first to make sure exclusions don't mess up
            if word_clean in headwords and word_clean not in definition_cleaned_unique:
                definition_cleaned_unique.append(word_clean)  # convert words to all-lowercase
        word_data[headword] = definition_cleaned_unique
    return word_data


# checks for 2 words matching (placeholder for handling inflection)
# returns true if match found for word1 in word2_list, false if not
def check_word_match(word1, word2_list):
    if word1 in word2_list:
        return True

    return False


# actually processes the words and definitions for links
def process_words(definition_data):
    links_data = {}  # used as a map of links between words

    headwords = definition_data.keys()  # feels more efficient to get this once

    for headword in headwords:
        definition = definition_data[headword]
        for word in definition:
            if check_word_match(word, headwords):  # link found
                if headword in links_data:  # already a link from this headword
                    links_data[headword].append(word)
                else:
                    links_data[headword] = [word]
    return links_data


# loads exclusions from data file
# exclusions are listed one per line
def load_exclusions(exclusions_filename, headwords):
    exclusions = []
    with open("exclusions.txt") as f:
        for line in f:
            exclusions.append(clean_word(line, headwords))
    return exclusions


# this removes instances of a word being linked to itself
def prune_self_links(links_map):
    pruned_links = {}
    for headword in links_map.keys():
        for linked_word in links_map[headword]:
            if linked_word != headword:  # not a self-link
                if headword in pruned_links:  # already a link from this headword
                    pruned_links[headword].append(linked_word)
                else:
                    pruned_links[headword] = [linked_word]
    return pruned_links


headwords_list = []
definitions_raw = load_entries("words.txt", headwords_list)  # load definitions

# this currently only excludes articles for testing, but will handle all exclusions
exclusions_list = load_exclusions("exclusions.txt", headwords_list)

definitions_cleaned = clean_entries(definitions_raw, exclusions_list, headwords_list)  # clean definitions

semantic_links_raw = process_words(definitions_cleaned)  # find links

semantic_links = prune_self_links(semantic_links_raw)  # get rid of words linking to themselves

for word in semantic_links.keys():  # debug code to output all raw links
    for dest_word in semantic_links[word]:
        print(word + " -> " + dest_word)
