import json
import os
import re

words_data = {}
words_data_raw = {}
plurals_map = {}
synonyms_map = {}
alt_spellings_map = {}
forms_map = {}

allowed_types = ["Noun", "Adjective", "Adverb", "Conjunction", "Preposition", "Interjection", "Verb", "Proper Noun"]


def find_word_in_partial_template(tmpl, startind):
    for arg in tmpl.split("|")[startind:]:
        if "=" not in arg and arg != "en":
            return arg


def handle_wikitemplate(wikitemplate):  # TODO cleanup
    # print("template found: "+wikitemplate)
    args = wikitemplate.replace("{", "").replace("}", "").split("|")
    # print("args: "+str(args))

    of_regex = re.compile(".* of$")

    if args[0] == "plural of":
        return "$$PLURAL$$" + find_word_in_partial_template(wikitemplate, 1)

    elif args[0] == "synonym of":
        return "$$SYNONYM$$" + find_word_in_partial_template(wikitemplate, 1)

    elif args[0] == "alternative spelling of" or args[0] == "alternative form of" \
            or args[0] == "archaic form of" or args[0] == "nonstandard spelling of" \
            or args[0] == "alt form" or args[0] == "alt case" or args[0] == "alt sp":
        return "$$ALTSPELL$$" + find_word_in_partial_template(wikitemplate, 1)

    elif args[0] == "n-g" or args[0] == "non-gloss definition":
        return parse_wikilinks(wikitemplate.split("|")[1].strip().replace("}}", ""))

    elif wikitemplate.startswith("{{l") or wikitemplate.startswith("{{link"):
        return parse_wikilinks(wikitemplate.split("|")[1].strip().replace("}}", ""))

    elif of_regex.match(args[0]):
        if "|en|" in wikitemplate:
            wikitemplate = wikitemplate.replace("|en|", "|")
        return "$$ALTFORM$$" + find_word_in_partial_template(wikitemplate.replace("}}", ""), 1)
    return ""


def handle_wikilink(wikilink):
    if "|" in wikilink:  # handle piped links
        wikilink = wikilink.split("|")[1]
    return wikilink.replace("[", "").replace("]", "")


def parse_wikitemplates(definition):
    processed_definition = ""
    wikitemplate_level = 0
    brace_state = 0
    last_brace_type = ""
    is_special = False
    special_str = ""
    wikitemplate = ""
    for char in definition:
        if char == "{":
            if last_brace_type == "" or last_brace_type == "{":
                brace_state += 1
                last_brace_type = "{"
            else:
                brace_state = 0
                last_brace_type = ""
        if char == "}" and (last_brace_type == "" or last_brace_type == "}"):
            if last_brace_type == "" or last_brace_type == "}":
                brace_state += 1
                last_brace_type = "}"
            else:
                brace_state = 0
                last_brace_type = ""
        if wikitemplate_level == 0 and char != "{":
            processed_definition = processed_definition + char
        if wikitemplate_level > 0:
            wikitemplate = wikitemplate + char
        if brace_state == 2:  # either entering or exiting wikitemplate
            if char == "{":
                wikitemplate_level += 1
            if char == "}":
                wikitemplate_level -= 1
            if wikitemplate_level == 0:  # exiting wikitemplate
                result = handle_wikitemplate(wikitemplate)
                if result.startswith("$$PLURAL") or result.startswith("$$SYNONYM") or result.startswith(
                        "$$ALTSPELL") or result.startswith("$$ALTFORM"):
                    is_special = True
                    special_str = result
                else:
                    processed_definition = processed_definition + result
            if wikitemplate_level == 1:  # entering new wikitemplate
                wikitemplate = "{{"
            brace_state = 0
            last_brace_type = ""
    if not is_special:
        return processed_definition
    else:
        return special_str


def parse_wikilinks(definition):
    processed_definition = ""
    in_wikilink = False
    brace_state = 0
    wikilink = ""
    for char in definition:
        if char == "[" and not in_wikilink:
            brace_state += 1
        if char == "]" and in_wikilink:
            brace_state += 1
        if not in_wikilink and char != "[":
            processed_definition = processed_definition + char
        if in_wikilink:
            wikilink = wikilink + char
        if brace_state == 2:  # either entering or exiting wikilink
            in_wikilink = not in_wikilink
            if not in_wikilink:  # exiting wikilink
                processed_definition = processed_definition + handle_wikilink(wikilink)
            if in_wikilink:  # entering new wikilink
                wikilink = "[["
            brace_state = 0
    return processed_definition


def process_definition(headword, definition_raw):
    definition_split = definition_raw.split("\n")
    definition_preproc = ""
    for line in definition_split:
        if not line.startswith("#*"):  # skip quotes
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
        # print(headword)
        # print(headword+": plural of "+definition.replace("$$PLURAL$$", ""))


def parse_file(filename):
    # data = None

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
                        process_definition(data['title'], entry3['text'])


base_path = "/Users/valiec/Desktop/word_data/English"

dirs = os.listdir(base_path)

for words_dir in dirs:
    if os.path.isdir(base_path + "/" + words_dir):
        if words_dir != "b":
            continue
        files = os.listdir(base_path + "/" + words_dir)
        for file in files:
            if file.endswith(".json"):
                parse_file(base_path + "/" + words_dir + "/" + file)

# parse_file("159.json")

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
