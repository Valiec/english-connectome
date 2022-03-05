import re


def find_word_in_partial_template(tmpl, startind):
    """takes a template string (minus the template name) and extracts the headword"""
    # print(tmpl)
    # print(startind)
    for arg in tmpl.split("|")[startind:]:
        if "=" not in arg and arg != "en":
            return arg
    return ""


def handle_wikitemplate(wikitemplate):  # TODO cleanup
    """Process a wikitemplate and locate any important information in it"""
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

    elif args[0] == "l" or args[0] == "link":
        return parse_wikilinks(wikitemplate.split("|")[1].strip().replace("}}", ""))

    elif of_regex.match(args[0]):
        if "|en|" in wikitemplate:
            wikitemplate = wikitemplate.replace("|en|", "|")
        return "$$ALTFORM$$" + find_word_in_partial_template(wikitemplate.replace("}}", ""), 1)
    return ""


def handle_wikilink(wikilink):
    """Process a wikilink to produce the word that would have been displayed on Wiktionary"""
    if "|" in wikilink:  # handle piped links
        wikilink = wikilink.split("|")[1]
    return wikilink.replace("[", "").replace("]", "")


def parse_wikitemplates(definition):
    """Parse a definition string for wikitemplates"""
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
    """Parse a definition string for wikilinks"""
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
