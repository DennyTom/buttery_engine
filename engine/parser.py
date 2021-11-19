import json
from functools import reduce

comma_separator = (lambda x, y: str(x) + ", " + str(y))
string_sum = (lambda x, y: str(x) + " + " + str(y))
newline_separator = (lambda x, y: str(x) + "\n" + str(y))

def parse_includes(keymap_def):
    includes = [f"#include {file}" for file in keymap_def["extra_dependencies"]]
    return reduce(newline_separator, includes)

def parse_new_keycodes(keymap_def):
    number_of_keys = len(keymap_def["keys"])
    if number_of_keys <= 8:
        hash_type = "uint8_t"
    elif number_of_keys <= 16:
        hash_type = "uint16_t"
    elif number_of_keys <= 32:
        hash_type = "uint32_t"
    elif number_of_keys <= 64:
        hash_type = "uint64_t"
    else:
        raise Exception("The engine currently supports only up to 64 keys.")

    keycodes = [f"#define H_{keycode} ((HASH_TYPE) 1 << {idx})" for idx, keycode in enumerate(keymap_def["keys"])]

    enum = f"""enum internal_keycodes {{
    {keymap_def["keys"][0]} = SAFE_RANGE,
    {reduce(comma_separator, keymap_def["keys"][1:])},
    FIRST_INTERNAL_KEYCODE = {keymap_def["keys"][0]},
    LAST_INTERNAL_KEYCODE = {keymap_def["keys"][-1]}
}};"""

    return f"""#define HASH_TYPE {hash_type}
{reduce(newline_separator, keycodes)}

{enum}"""

def parse_pseudolayers(keymap_def):
    return f"""enum pseudolayers {{
    {reduce(comma_separator, [pseudolayer["name"] for pseudolayer in keymap_def["pseudolayers"]])}
}};"""

def buttery_parser(input_file):
    with open(input_file, "r") as file:
        keymap_def = json.load(file)

    includes = parse_includes(keymap_def)
    keycodes = parse_new_keycodes(keymap_def)
    pseudolayers = parse_pseudolayers(keymap_def)
    keyboard_parameters = ""
    keymaps = ""
    buffers = ""
    chords = ""
    return includes, keycodes, pseudolayers, keyboard_parameters, keymaps, buffers, chords