from engine.utils import plus_separator, newline_separator, comma_separator, my_format, unpack_by_chars
from engine.keycodes import expand_keycode
from functools import reduce

chord_with_counter = """uint8_t counter_{index} = 0;
uint8_t state_{index} = 0;
const struct Chord chord_{index} PROGMEM = {{
    {keycodes_hash},
    {on_pseudolayer},
    &state_{index},
    &counter_{index},
    {value1},
    {value2},
    {function}
}};
"""

chord_without_counter = """uint8_t state_{index} = 0;
const struct Chord chord_{index} PROGMEM = {{
    {keycodes_hash},
    {on_pseudolayer},
    &state_{index},
    NULL,
    {value1},
    {value2},
    {function}
}};
"""

chords = []
strings = []

def add_simple_chord(pseudolayer, original_keycode, chord_keys):
    global chords
    global strings
    
    keycode = expand_keycode(original_keycode)
    hash = reduce(plus_separator, [f"H_{key}" for key in chord_keys])

    if keycode.startswith("KC"):
        chords.append(my_format(s = chord_without_counter,
             index = len(chords),
             on_pseudolayer = pseudolayer,
             keycodes_hash = hash,
             value1 = keycode,
             value2 = 0,
             function = "single_dance"))
    elif keycode.startswith("STR"):
        s = unpack_by_chars(original_keycode, '(', ')')
        if s[0] == '"':
            s = unpack_by_chars(s, '"', '"')
        elif s[0] == "'":
            s = unpack_by_chars(s, "'", "'")
        
        chords.append(my_format(s = chord_without_counter,
             index = len(chords),
             on_pseudolayer = pseudolayer,
             keycodes_hash = hash,
             value1 = len(strings),
             value2 = 0,
             function = "string_in"))

        strings.append(s)
    elif keycode.startswith("MO("):
        to_pseudolayer = unpack_by_chars(original_keycode, '(', ')')

        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = to_pseudolayer, 
            value2 = 0,
            function = "temp_pseudolayer"))
    elif keycode.startswith("DF"):
        to_pseudolayer = unpack_by_chars(original_keycode, '(', ')')

        chords.append(my_format(s = chord_without_counter,
        index = len(chords),
        on_pseudolayer = pseudolayer,
        keycodes_hash = hash,
        value1 = to_pseudolayer, 
        value2 = 0,
        function = "perm_pseudolayer"))

def parse_chords(keymap_def):
    global chords
    global strings

    for pseudolayer in keymap_def["pseudolayers"]:
        for chord in pseudolayer["chords"]:
            if chord["type"] == "simple":
                add_simple_chord(pseudolayer["name"], chord["keycode"], chord["chord"])
            elif chord["type"] == "visual":
                pass
            elif chord["type"] == "visual_array":
                pass
            elif chord["type"] == "chord_set":
                pass

    chord_list = reduce(comma_separator, [f"&chord_{i}" for i in range(len(chords))])
    strings = [f"\"{x}\"" for x in strings]

    result = f"""{reduce(newline_separator, chords)}
#define NUMBER_OF_CHORDS {len(chords)}
const struct Chord* const list_of_chords[] PROGMEM = {{
    {chord_list}
}};

const char * const strings[] PROGMEM = {{
    {reduce(comma_separator, strings)}
}};
"""

    return result