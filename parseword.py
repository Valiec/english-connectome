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
    if "=" not in arg:
      return arg

def handle_wikitemplate(wikitemplate):  # TODO fix this!!!
  #print("template found: "+wikitemplate)

  of_regex = re.compile("\{\{.* of$")

  if wikitemplate.startswith("{{plural of|en|"):
    return "$$PLURAL$$"+find_word_in_partial_template(wikitemplate, 2)
  elif wikitemplate.startswith("{{plural of|"):
    return "$$PLURAL$$"+find_word_in_partial_template(wikitemplate, 1)
  elif wikitemplate.startswith("{{synonym of|"):
    return "$$SYNONYM$$"+find_word_in_partial_template(wikitemplate, 1)
  elif wikitemplate.startswith("{{alternative spelling of|en") or wikitemplate.startswith("{{alternative form of|en") or wikitemplate.startswith("{{archaic form of|en") or wikitemplate.startswith("{{nonstandard spelling of|en"):
    return "$$ALTSPELL$$"+find_word_in_partial_template(wikitemplate, 2)
  elif wikitemplate.startswith("{{alternative spelling of|") or wikitemplate.startswith("{{alternative form of|") or wikitemplate.startswith("{{nonstandard spelling of|") or wikitemplate.startswith("{{archaic form of|"):
    return "$$ALTSPELL$$"+find_word_in_partial_template(wikitemplate, 1)
  elif wikitemplate.startswith("{{n-g") or wikitemplate.startswith("{{non-gloss definition"):
    return parse_wikilinks(wikitemplate.split("|")[1].strip().replace("}}", ""))
  elif wikitemplate.startswith("{{l") or wikitemplate.startswith("{{link"):
    return parse_wikilinks(wikitemplate.split("|")[1].strip().replace("}}", ""))
  elif wikitemplate.startswith("{{alternative spelling of|en") or wikitemplate.startswith("{{alternative form of|en") or wikitemplate.startswith("{{archaic form of|en") or wikitemplate.startswith("{{nonstandard spelling of|en") or wikitemplate.startswith("{{alt form|en") or wikitemplate.startswith("{{alt case|en") or wikitemplate.startswith("{{alt sp|en"):
    return "$$ALTSPELL$$"+find_word_in_partial_template(wikitemplate, 2)
  elif wikitemplate.startswith("{{alternative spelling of") or wikitemplate.startswith("{{alternative form of") or wikitemplate.startswith("{{nonstandard spelling of") or wikitemplate.startswith("{{archaic form of") or wikitemplate.startswith("{{alt form") or wikitemplate.startswith("{{alt case") or wikitemplate.startswith("{{alt sp"):
    return "$$ALTSPELL$$"+find_word_in_partial_template(wikitemplate, 1)
  elif of_regex.match(wikitemplate.split("|")[0]):
    if "|en|" in wikitemplate:
      wikitemplate = wikitemplate.replace("|en|", "|")
    return "$$ALTFORM$$"+find_word_in_partial_template(wikitemplate.replace("}}", ""), 1)
  return ""

def handle_wikilink(wikilink):
  #print("link found: "+wikilink)
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
        brace_state+=1
        last_brace_type = "{"
      else:
        brace_state = 0
        last_brace_type = ""
    if char == "}" and (last_brace_type == "" or last_brace_type == "}"):
      if last_brace_type == "" or last_brace_type == "}":
        brace_state+=1
        last_brace_type = "}"
      else:
        brace_state = 0
        last_brace_type = ""
    if wikitemplate_level == 0 and char != "{":
      processed_definition = processed_definition+char
    if wikitemplate_level > 0:
      wikitemplate= wikitemplate+char
    if brace_state == 2: # either entering or exiting wikitemplate
      if char == "{":
        wikitemplate_level+=1
      if char == "}":
        wikitemplate_level-=1
      if wikitemplate_level == 0: # exiting wikitemplate
        result = handle_wikitemplate(wikitemplate)
        if result.startswith("$$PLURAL") or result.startswith("$$SYNONYM") or result.startswith("$$ALTSPELL") or result.startswith("$$ALTFORM"):
          is_special = True
          special_str = result
        else:
          processed_definition = processed_definition+result
      if wikitemplate_level == 1: # entering new wikitemplate
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
      brace_state+=1
    if char == "]" and in_wikilink:
      brace_state+=1
    if not in_wikilink and char != "[":
      processed_definition = processed_definition+char
    if in_wikilink:
      wikilink = wikilink+char
    if brace_state == 2: # either entering or exiting wikilink
      in_wikilink = not in_wikilink
      if not in_wikilink: # exiting wikilink
        processed_definition = processed_definition+handle_wikilink(wikilink)
      if in_wikilink: # entering new wikilink
        wikilink = "[["
      brace_state = 0
  return processed_definition

def process_definition(headword, definition_raw):
  definition = definition_raw.replace("\n", " ")
  #print(headword+": "+definition)
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
    words_data_raw[headword] = definition_raw.replace("\n", " ")
    #print(headword)
    #print(headword+": plural of "+definition.replace("$$PLURAL$$", ""))

def parse_file(filename):

  data = None

  with open(filename) as f:
    data = json.load(f)

  for entry in data['text']:
    if not 'subSections' in entry:
      continue
    for entry2 in entry['subSections']:
      if entry2['title'] == "English":
        if not 'subSections' in entry2:
          continue
        for entry3 in entry2['subSections']:
          if entry3['title'] in allowed_types:
              process_definition(data['title'], entry3['text'])

basepath = "/Users/valiec/Desktop/word_data/English"

dirs = os.listdir(basepath)

for dir in dirs:
  if os.path.isdir(basepath+"/"+dir):
    if dir != "b":
      continue
    files = os.listdir(basepath+"/"+dir)
    for file in files:
      if file.endswith(".json"):
        parse_file(basepath+"/"+dir+"/"+file)

with open("word_data_out.txt", "w") as f:
  for word in words_data.keys():
    f.write(word+"\t"+words_data[word]+"\n")

with open("word_data_out_raw.txt", "w") as f:
  for word in words_data.keys():
    f.write(word+"\t"+words_data_raw[word]+"\n")

with open("plurals_out.txt", "w") as f:
  for word in plurals_map.keys():
    f.write(word+"\t"+plurals_map[word]+"\n")

with open("synonyms_out.txt", "w") as f:
  for word in synonyms_map.keys():
    f.write(word+"\t"+synonyms_map[word]+"\n")

with open("alt_spellings_out.txt", "w") as f:
  for word in alt_spellings_map.keys():
    f.write(word+"\t"+alt_spellings_map[word]+"\n")

with open("forms_out.txt", "w") as f:
  for word in forms_map.keys():
    f.write(word+"\t"+forms_map[word]+"\n")
