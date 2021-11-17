#!/usr/bin/env python3

import json
from functools import reduce 
from chord import *
import sys

comma_separator = (lambda x, y: str(x) + ", " + str(y))
string_sum = (lambda x, y: str(x) + " + " + str(y))
newline_separator = (lambda x, y: str(x) + "\n" + str(y))

def add_includes(data):
    output_buffer = ""
    if not ("do_not_include_QMK" in data["parameters"] and data["parameters"]["do_not_include_QMK"] == True):
        output_buffer += "#include QMK_KEYBOARD_H"
    if len(data["extra_dependencies"]) > 0:
        for dependecy in data["extra_dependencies"]:
            output_buffer += '\n#include "' + dependecy
    
    return output_buffer

def add_parameters(data):
    number_of_keys = len(data["keys"])
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
    
    parameters = data["parameters"]

    output_buffer = """#define CHORD_TIMEOUT {}
#define DANCE_TIMEOUT {}
#define LEADER_TIMEOUT {}
#define TAP_TIMEOUT {}
#define LONG_PRESS_MULTIPLIER {}
#define DYNAMIC_MACRO_MAX_LENGTH {}
#define COMMAND_MAX_LENGTH {}
#define STRING_MAX_LENGTH {}
#define LEADER_MAX_LENGTH {}
#define HASH_TYPE {}
#define NUMBER_OF_KEYS {}
#define DEFAULT_PSEUDOLAYER {}""".format(
        parameters["chord_timeout"],
        parameters["dance_timeout"],
        parameters["leader_timeout"],
        parameters["tap_timeout"],
        parameters["long_press_multiplier"],
        parameters["dynamic_macro_max_length"],
        parameters["command_max_length"],
        parameters["string_max_length"],
        parameters["leader_max_length"],
        hash_type,
        len(data["keys"]),
        parameters["default_pseudolayer"]
    )
    
    return output_buffer

def add_keycodes(data):
    output_buffer = ""
    
    if not len(data["keys"]) == len(set(data["keys"])):
        raise Exception("The keys must have unique names")
    
    for key, counter in zip(data["keys"], range(0, len(data["keys"]))):
        output_buffer += "#define H_" + key + " ((HASH_TYPE) 1 << " + str(counter) + ")\n"
    output_buffer += "\n"
    
    output_buffer += """enum internal_keycodes {{
    {} = SAFE_RANGE,
    {},
    FIRST_INTERNAL_KEYCODE = {},
    LAST_INTERNAL_KEYCODE = {}
}};""".format(
        data["keys"][0],
        reduce(comma_separator, [key for key in data["keys"][1:]]),
        data["keys"][0],
        data["keys"][-1]
    )
    
    return output_buffer

def add_pseudolayers(data):
    output_buffer = ""
    
    if len(data["pseudolayers"]) == 0:
        raise Exception("You didn't define any pseudolayers")
    
    if not len([pseudolayer["name"] for pseudolayer in data["pseudolayers"]]) == len(set([pseudolayer["name"] for pseudolayer in data["pseudolayers"]])):
        raise Exception("The pseudolayers must have unique names")
    
    pseudolayers = data["pseudolayers"]
    if not "ALWAYS_ON" in [layer["name"] for layer in pseudolayers]:
        pseudolayers += [{"name": "ALWAYS_ON", "chords": []}] # the engine expects ALWAYS_ON to exist
    
    output_buffer += "enum pseudolayers {\n    " + reduce(comma_separator, [layer["name"] for layer in pseudolayers]) + "\n};"
    
    return output_buffer

def add_layers(data):
    output_buffer = "const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {\n"
    for layer, counter in zip(data["layers"], range(0,len(data["layers"]))):
        if layer["type"] == "auto":
            output_buffer += "    [" + str(counter) + "] = " + data["parameters"]["layout_function_name"] + "(" + reduce(comma_separator, [key for key in data["keys"]]) + "),\n"
        else:
            output_buffer += "    [" + str(counter) + "] = " + data["parameters"]["layout_function_name"] + "(" + reduce(comma_separator, [key for key in layer["keycodes"]]) + "),\n"
    output_buffer += "};\nsize_t keymapsCount = " + str(len(data["layers"])) + ";"
    
    return output_buffer

def prep_buffers(data):
    parameters = data["parameters"]
    output_buffer = """uint8_t keycodes_buffer_array[] = {{
    {}
}};

uint8_t command_buffer[] = {{
    {}
}};

uint16_t leader_buffer[] = {{
    {}
}};

uint8_t dynamic_macro_buffer[] = {{
    {}
}};""".format(
        reduce(comma_separator, ["0"] * len(data["keys"])),
        reduce(comma_separator, ["0"] * parameters["command_max_length"]),
        reduce(comma_separator, ["0"] * parameters["leader_max_length"]),
        reduce(comma_separator, ["0"] * parameters["dynamic_macro_max_length"])
    )
    
    return output_buffer

def parse_chords(data):
    keyboard_part_2 = ""
    strings = []
    number_of_strings = 0
    number_of_chords = 0
    
    for pseudolayer in data["pseudolayers"]:
        name = pseudolayer["name"]
        for chord in pseudolayer["chords"]:
            if chord["type"] == "chord_set":
                keycodes = reduce(comma_separator, [word for word in chord["keycodes"]])
                [keyboard_part_2, number_of_chords, number_of_strings, strings] = add_chord_set(name, keycodes, chord["set"], data, keyboard_part_2, number_of_chords, number_of_strings, strings)
            if chord["type"] == "visual_array":
                [keyboard_part_2, number_of_chords, number_of_strings, strings] = add_dictionary(name, chord["keys"], chord["dictionary"], keyboard_part_2, number_of_chords, number_of_strings, strings)
            if chord["type"] == "visual":
                keycodes = reduce(comma_separator, [word for word in chord["chord"]])
                [keyboard_part_2, number_of_chords, number_of_strings, strings] = secret_chord(name, chord["keycode"], keycodes, data, keyboard_part_2, number_of_chords, number_of_strings, strings)
            elif chord["type"] == "simple":
                keycodes = reduce(string_sum, ["H_" + word for word in chord["chord"]])
                [keyboard_part_2, number_of_chords, number_of_strings, strings] = add_key(name, keycodes, chord["keycode"], keyboard_part_2, number_of_chords, number_of_strings, strings)
    keyboard_part_2 += "\n"
    
    keyboard_part_2 += "const struct Chord* const list_of_chords[] PROGMEM = {\n"
    keyboard_part_2 += "    " + reduce(comma_separator, ["&chord_" + str(i) for i in range(0, number_of_chords)]) + "\n};\n\n"
    
    if len(data["leader_sequences"]) > 0:
        keyboard_part_2 += reduce(newline_separator, [sequence["function"] for sequence in data["leader_sequences"]]) + "\n\n"
        keyboard_part_2 += "const uint16_t leader_triggers[][LEADER_MAX_LENGTH] PROGMEM = {\n"
        for sequence in data["leader_sequences"]:
            keyboard_part_2 += "    {" + reduce(comma_separator, sequence["sequence"] + ["0"] * (data["parameters"]["leader_max_length"] - len(sequence["sequence"]))) + "},\n"
        keyboard_part_2 += "};\n\n"
        keyboard_part_2 += "void (*leader_functions[]) (void) = {\n"
        keyboard_part_2 += "    " + reduce(comma_separator, ["&" + sequence["name"] for sequence in data["leader_sequences"]]) + "\n"
        keyboard_part_2 += "};\n"
    else:
        keyboard_part_2 += "const uint16_t** const leader_triggers PROGMEM = NULL;\n"
        keyboard_part_2 += "void (*leader_functions[]) (void) = {};\n"
    keyboard_part_2 += "\n"
    
    keyboard_part_2 += "#define NUMBER_OF_CHORDS " + str(number_of_chords) + "\n"
    keyboard_part_2 += "#define NUMBER_OF_LEADER_COMBOS " + str(len(data["leader_sequences"]))
    
    return keyboard_part_2

def parse_strings_for_chords(data):
    keyboard_part_1 = ""
    
    for string, i in zip(strings, range(0, len(strings))):
        keyboard_part_1 += "const char string_" + str(i) + " [] PROGMEM = \"" + string + "\";\n"

    keyboard_part_1 += "\n"
    keyboard_part_1 += "const char * const strings[] PROGMEM = {\n"
    if len(strings) > 0:
        keyboard_part_1 += "    " + reduce(comma_separator, ["string_" + str(i) for i in range(0, len(strings))]) 
    keyboard_part_1 += "\n};"
    
    return keyboard_part_1

def main():
    if len(sys.argv) != 3:
        raise Exception("Wrong number of arguments.\n\nUsage: python parser.py keymap.json keymap.c")
    
    input_filepath = sys.argv[1]
    output_filepath = sys.argv[2]
    
    template_filepath = "template.txt"
    
    with open(input_filepath, "r") as read_file:
        with open(template_filepath, "r") as template_file:
            with open(output_filepath, "w") as write_file:
                data = json.load(read_file)
                
                output_buffer = template_file.read().format(
                    includes = add_includes(data),
                    keycodes = add_keycodes(data),
                    pseudolayers = add_pseudolayers(data),
                    keyboard_parameters = add_parameters(data),
                    keymaps = add_layers(data),
                    buffers = prep_buffers(data),
                    chords = parse_chords(data)
                )
                
                write_file.write(output_buffer)

if __name__ == "__main__":
    main()