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
    elif keycode.startswith("TO"):
        to_pseudolayer = unpack_by_chars(original_keycode, '(', ')')

        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = to_pseudolayer, 
            value2 = 0,
            function = "switch_layer"))
    elif keycode.startswith("OSK"):
        keycode = expand_keycode(unpack_by_chars(original_keycode, '(', ')'))

        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = keycode, 
            value2 = 0,
            function = "one_shot_key"))
    elif keycode.startswith("OSL"):
        to_pseudolayer = unpack_by_chars(original_keycode, '(', ')')

        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = to_pseudolayer, 
            value2 = 0,
            function = "one_shot_layer"))
    elif keycode.startswith("KK"):
        keycodes = [expand_keycode(y.strip()) for y in unpack_by_chars(original_keycode, '(', ')').split(",")]

        chords.append(my_format(s = chord_with_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = keycodes[0], 
            value2 = keycodes[1],
            function = "key_key_dance"))
    elif keycode.startswith("KL"):
        keycode = expand_keycode(unpack_by_chars(original_keycode, '(', ')').split(",")[0].strip())
        to_pseudolayer = unpack_by_chars(original_keycode, '(', ')').split(",")[1].strip()

        chords.append(my_format(s = chord_with_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = keycode, 
            value2 = to_pseudolayer,
            function = "key_layer_dance"))
    elif keycode.startswith("KM"):
        keycodes = [expand_keycode(y.strip()) for y in unpack_by_chars(original_keycode, '(', ')').split(",")]

        chords.append(my_format(s = chord_with_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = keycodes[0], 
            value2 = keycodes[1],
            function = "key_mod_dance"))
    elif keycode.startswith("AS"):
        keycode = expand_keycode(unpack_by_chars(original_keycode, '(', ')'))

        chords.append(my_format(s = chord_with_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = keycode, 
            value2 = 0,
            function = "autoshift_dance"))
    elif keycode.startswith("AT"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "autoshift_toggle"))
    elif keycode.startswith("LOCK"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "lock"))
    elif keycode.startswith("CMD"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "command"))
    elif keycode.startswith("LEAD"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "leader"))
    elif keycode.startswith("M("):
        fnc = unpack_by_chars(original_keycode, '(', ')').split(",")[0].strip()
        value1 = unpack_by_chars(original_keycode, '(', ')').split(",")[1].strip()
        value2 = unpack_by_chars(original_keycode, '(', ')').split(",")[2].strip()

        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = value1, 
            value2 = value2,
            function = fnc))
    elif keycode.startswith("MK"):
        keycodes = [expand_keycode(y.strip()) for y in unpack_by_chars(original_keycode, '(', ')').split(",")]
        key_ins = reduce(newline_separator, [f"{12*' '}key_in({y});" for y in keycodes])
        key_outs = reduce(newline_separator, [f"{12*' '}key_out({y});" for y in keycodes])
        fnc = f"""void function_{len(chords)}(const struct Chord* self) {{
    switch (*self->state) {{
        case ACTIVATED:
{key_ins}
            break;
        case DEACTIVATED:
{key_outs}
            *self->state = IDLE;
            break;
        case RESTART:
{key_outs}
            break;
        default:
            break;
    }};
}}
"""
        chords.append(fnc + my_format(s = chord_with_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = f"function_{len(chords)}"))
    elif keycode.startswith("D("):
        keycodes = [expand_keycode(y.strip()) for y in unpack_by_chars(original_keycode, '(', ')').split(",")]
        key_ins = reduce(newline_separator, [f"{16*' '}case {i+1}:\n{20*' '}key_in({y});\n{20*' '}break;" for i, y in enumerate(keycodes)])
        key_outs = reduce(newline_separator, [f"{16*' '}case {i+1}:\n{20*' '}key_out({y});\n{20*' '}break;" for i, y in enumerate(keycodes)])
        fnc = f"""void function_{len(chords)}(const struct Chord* self) {{
    switch (*self->state) {{
        case ACTIVATED:
            *self->counter = *self->counter + 1;
            break;
        case PRESS_FROM_ACTIVE:
            switch (*self->counter) {{
{key_ins}
                default:
                    break;
            }}
            *self->state = FINISHED_FROM_ACTIVE;
            break;
        case FINISHED:
            switch (*self->counter) {{
{key_outs}
                default:
                    break;
            }}
            *self->counter = 0;
            *self->state = IDLE;
            break;
        case RESTART:
            switch (*self->counter) {{
{key_outs}
                default:
                    break;
            }}
            *self->counter = 0;
            break;
        default:
            break;
    }};
}}
"""
        chords.append(fnc + my_format(s = chord_with_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = f"function_{len(chords)}"))
    elif keycode.startswith("DM_RECORD"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "dynamic_macro_record"))
    elif keycode.startswith("DM_NEXT"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "dynamic_macro_next"))
    elif keycode.startswith("DM_END"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "dynamic_macro_end"))
    elif keycode.startswith("DM_PLAY"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "dynamic_macro_play"))
    elif keycode.startswith("CLEAR_KB"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "clear"))
    elif keycode.startswith("RESET"):
        chords.append(my_format(s = chord_without_counter,
            index = len(chords),
            on_pseudolayer = pseudolayer,
            keycodes_hash = hash,
            value1 = 0, 
            value2 = 0,
            function = "reset"))

def add_visual_chord(pseudolayer, keycode, chord, keys):
    sum_chord = [keys[i] for i, x in enumerate(chord) if x == "X" or x == "x"]
    add_simple_chord(pseudolayer, keycode, sum_chord)

def parse_chords(keymap_def):
    global chords
    global strings

    for pseudolayer in keymap_def["pseudolayers"]:
        for chord in pseudolayer["chords"]:
            if chord["type"] == "simple":
                add_simple_chord(pseudolayer["name"], chord["keycode"], chord["chord"])
            elif chord["type"] == "visual":
                add_visual_chord(pseudolayer["name"], chord["keycode"], chord["chord"], keymap_def["keys"])
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
}};"""

    return result