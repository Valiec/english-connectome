# library for sem_links.py

def check_word_match(word1, word2_list):
    """checks for 2 words matching (placeholder for handling inflection)

    returns true if match found for word1 in word2_list, false if not"""
    if word1 in word2_list:
        return True

    return False


def process_words(definition_data):
    """actually processes the words and definitions for links"""
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


def prune_self_links(links_map):
    """this removes instances of a word being linked to itself"""
    pruned_links = {}
    for headword in links_map.keys():
        for linked_word in links_map[headword]:
            if linked_word != headword:  # not a self-link
                if headword in pruned_links:  # already a link from this headword
                    pruned_links[headword].append(linked_word)
                else:
                    pruned_links[headword] = [linked_word]
    return pruned_links
