import json
from wiktionary_parsing import *

allowed_types = ["Noun", "Adjective", "Adverb", "Conjunction", "Preposition", "Interjection", "Verb", "Proper Noun"]


def process_definition(headword, definition_raw, plurals_map, synonyms_map, forms_map, alt_spellings_map, words_data,
                       words_data_raw):
    """Parses a Wiktionary definition and adds the relevant data to the maps passed in"""
    definition_split = definition_raw.split("\n")
    definition_preproc = ""
    for line in definition_split:
        if not line.startswith("#*") and not line.startswith("##*"):  # skip quotes
            definition_preproc += line
    definition = definition_preproc.replace("\n", " ")
    # print(headword+": "+definition)
    definition = parse_wikilinks(definition)
    definition = parse_wikitemplates(definition)
    if definition.startswith("$$PLURAL"):
        plurals_map[headword] = definition.replace("$$PLURAL$$", "")
    elif definition.startswith("$$SYNONYM"):
        synonyms_map[headword] = definition.replace("$$SYNONYM$$", "")
    elif definition.startswith("$$ALTSPELL"):
        alt_spellings_map[headword] = definition.replace("$$ALTSPELL$$", "")
    elif definition.startswith("$$ALTFORM"):
        forms_map[headword] = definition.replace("$$ALTFORM$$", "")
    else:
        words_data[headword] = definition
        words_data_raw[headword] = definition_preproc.replace("\n", "$$")


def parse_file(filename, plurals_map, synonyms_map, forms_map, alt_spellings_map, words_data, words_data_raw):
    # data = None

    """Parses a Wiktionary json file and adds the relevant data to the maps passed in"""

    with open(filename) as data_file:
        data = json.load(data_file)

    for entry in data['text']:
        if 'subSections' not in entry:
            continue
        for entry2 in entry['subSections']:
            if entry2['title'] == "English":
                if 'subSections' not in entry2:
                    continue
                for entry3 in entry2['subSections']:
                    if entry3['title'] in allowed_types:
                        process_definition(data['title'], entry3['text'], plurals_map, synonyms_map, forms_map,
                                           alt_spellings_map, words_data, words_data_raw)
