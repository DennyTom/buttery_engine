import json
from functools import reduce

comma_separator = (lambda x, y: str(x) + ", " + str(y))
string_sum = (lambda x, y: str(x) + " + " + str(y))
newline_separator = (lambda x, y: str(x) + "\n" + str(y))

def parse_includes(keymap_def):
    includes = [f"#include {file}" for file in keymap_def["extra_dependencies"]]
    includes = reduce(newline_separator, includes)
    return includes

def buttery_parser(input_file):
    with open(input_file, "r") as file:
        keymap_def = json.load(file)

    includes = parse_includes(keymap_def)
    keycodes = ""
    pseudolayers = ""
    keyboard_parameters = ""
    keymaps = ""
    buffers = ""
    chords = ""
    return includes, keycodes, pseudolayers, keyboard_parameters, keymaps, buffers, chords