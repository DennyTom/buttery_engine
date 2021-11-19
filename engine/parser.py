import json
from functools import reduce

comma_separator = (lambda x, y: str(x) + ", " + str(y))
newline_comma_separator = (lambda x, y: str(x) + ",\n\t" + str(y))
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
#define NUMBER_OF_KEYS {number_of_keys}

{reduce(newline_separator, keycodes)}

{enum}"""

def parse_pseudolayers(keymap_def):
    return f"""enum pseudolayers {{
    {reduce(comma_separator, [pseudolayer["name"] for pseudolayer in keymap_def["pseudolayers"]])}
}};"""

def parse_layers(keymap_def):
    layout_name = keymap_def["parameters"]["layout_function_name"]
    layers = []
    for idx, layer in enumerate(keymap_def["layers"]):
        if layer["type"] == "auto":
            keys = reduce(comma_separator, keymap_def["keys"])
            layers.append(f"[{idx}] = {layout_name}({keys})")
    return reduce(newline_comma_separator, layers)

def parse_keyboard_parameters(keymap_def):
    params = keymap_def["parameters"]
    return f"""#define CHORD_TIMEOUT {params["chord_timeout"]}
#define DANCE_TIMEOUT {params["dance_timeout"]}
#define LEADER_TIMEOUT {params["leader_timeout"]}
#define TAP_TIMEOUT {params["tap_timeout"]}
#define LONG_PRESS_MULTIPLIER {params["long_press_multiplier"]}
#define DYNAMIC_MACRO_MAX_LENGTH {params["dynamic_macro_max_length"]}
#define COMMAND_MAX_LENGTH {params["command_max_length"]}
#define STRING_MAX_LENGTH {params["string_max_length"]}
#define LEADER_MAX_LENGTH {params["leader_max_length"]}
#define DEFAULT_PSEUDOLAYER {params["default_pseudolayer"]}

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {{
    {parse_layers(keymap_def)}
}};
size_t keymapsCount = {len(keymap_def["layers"])};

uint8_t keycodes_buffer_array[] = {{
    {reduce(comma_separator, [0 for _ in range(len(keymap_def["keys"]))])}
}};

uint8_t command_buffer[] = {{
    {reduce(comma_separator, [0 for _ in range(params["command_max_length"])])}
}};

uint16_t leader_buffer[] = {{
    {reduce(comma_separator, [0 for _ in range(params["leader_max_length"])])}
}};

uint8_t dynamic_macro_buffer[] = {{
    {reduce(comma_separator, [0 for _ in range(params["dynamic_macro_max_length"])])}
}};"""

def buttery_parser(input_file):
    with open(input_file, "r") as file:
        keymap_def = json.load(file)

    includes = parse_includes(keymap_def)
    keycodes = parse_new_keycodes(keymap_def)
    pseudolayers = parse_pseudolayers(keymap_def)
    keyboard_parameters = parse_keyboard_parameters(keymap_def)
    keymaps = ""
    buffers = ""
    chords = ""
    return includes, keycodes, pseudolayers, keyboard_parameters, keymaps, buffers, chords