from functools import reduce
import re
import string

comma_separator = (lambda x, y: str(x) + ", " + str(y))
string_sum = (lambda x, y: str(x) + " + " + str(y))
newline_separator = (lambda x, y: str(x) + "\n" + str(y))

def stitch(*args):
    return reduce(newline_separator, list(args))

class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

def my_format(**kwargs):
    formatter = string.Formatter()
    mapping = FormatDict(kwargs)
    return formatter.vformat(kwargs["s"], (), mapping)

strings = []
number_of_strings = -1

def top_level_split(s):
    """
    Split `s` by top-level commas only. Commas within parentheses are ignored.
    """
    
    # Parse the string tracking whether the current character is within
    # parentheses.
    balance = 0
    parts = []
    part = ""
    
    for i in range(len(s)):
        c = s[i]
        part += c
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
        elif c == ',' and balance == 0 and not s[i+1] == ',':
            part = part[:-1].strip()
            parts.append(part)
            part = ""
    
    # Capture last part
    if len(part):
        parts.append(part.strip())
    
    return parts

state = "uint8_t state_{index} = 0;\n"
chord = """
    const struct Chord chord_{index} PROGMEM = {{
    {keycodes_hash},
    {on_pseudolayer},
    &state_{index},
    {counter_link},
    {value1},
    {value2},
    {function}
}};
"""

chord_with_counter = state + "uint8_t counter_{index} = 0;\n" + my_format(s = chord, counter_link = "&counter_{index}")
chord_without_counter = state + my_format(s = chord, counter_link = "NULL")

KC = my_format(
    S = chord_without_counter,
    index = index,
    on_pseudolayer = on_pseudolayer,
    keycodes_hash = keycodes_hash,
    value1 = keycode,
    value2 = 0,
    function = "single_dance"
)

AS = my_format(
    S = chord_with_counter,
    index = index,
    on_pseudolayer = on_pseudolayer,
    keycodes_hash = keycodes_hash,
    value1 = keycode, 
    value2 = 0,
    function = "autoshift_dance"
)



def AT(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "autoshift_toggle"), index+1]

def KL(on_pseudolayer, keycodes_hash, keycode, to_pseudolayer, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_with_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = keycode, 
        value2 = to_pseudolayer,
        function = "key_layer_dance"), index+1]

def KK(on_pseudolayer, keycodes_hash, keycode1, keycode2, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_with_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = keycode1, 
        value2 = keycode2,
        function = "key_key_dance"), index+1]

def KM(on_pseudolayer, keycodes_hash, keycode, to_pseudolayer, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = keycode, 
        value2 = to_pseudolayer,
        function = "key_mod_dance"), index+1]

def MO(on_pseudolayer, keycodes_hash, to_pseudolayer, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = to_pseudolayer, 
        value2 = 0,
        function = "temp_pseudolayer"), index+1]

def MO_alt(on_pseudolayer, keycodes_hash, from_pseudolayer, to_pseudolayer, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = to_pseudolayer, 
        value2 = from_pseudolayer,
        function = "single_dance"), index+1]

def LOCK(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "lock"), index+1]

def DF(on_pseudolayer, keycodes_hash, to_pseudolayer, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = to_pseudolayer, 
        value2 = 0,
        function = "perm_pseudolayer"), index+1]

def TO(on_pseudolayer, keycodes_hash, to_pseudolayer, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = to_pseudolayer, 
        value2 = 0,
        function = "switch_layer"), index+1]

def OSK(on_pseudolayer, keycodes_hash, keycode, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = keycode, 
        value2 = 0,
        function = "one_shot_key"), index+1]

def OSL(on_pseudolayer, keycodes_hash, to_pseudolayer, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = to_pseudolayer, 
        value2 = 0,
        function = "one_shot_layer"), index+1]

def CMD(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "command"), index+1]

def DM_RECORD(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "dynamic_macro_record"), index+1]

def DM_NEXT(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "dynamic_macro_next"), index+1]

def DM_END(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "dynamic_macro_end"), index+1]

def DM_PLAY(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "dynamic_macro_play"), index+1]

def LEAD(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "leader"), index+1]

def CLEAR(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "clear"), index+1]

def RESET(on_pseudolayer, keycodes_hash, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = 0, 
        value2 = 0,
        function = "reset"), index+1]

def STR(on_pseudolayer, keycodes_hash, string_input, output_buffer, index, number_of_strings, strings):
    a = my_format(S = chord_without_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = number_of_strings, 
        value2 = 0,
        function = "string_in")
    b = index + 1
    return [output_buffer + a, b, number_of_strings + 1, strings + [string_input]]

def M(on_pseudolayer, keycodes_hash, value1, value2, fnc, output_buffer, index):
    return [output_buffer + "\n" + my_format(S = chord_with_counter,
        index = index,
        on_pseudolayer = on_pseudolayer,
        keycodes_hash = keycodes_hash,
        value1 = value1, 
        value2 = value2,
        function = fnc), index+1]

alternate_keycodes = {
    "`": "GRAVE",
    "-": "MINUS",
    "=": "EQUAL",
    "[": "LBRACKET",
    "]": "RBRACKET",
    "\\": "BSLASH",
    ";": "SCOLON",
    "'": "QUOTE",
    ",": "COMMA",
    ".": "DOT",
    "/": "SLASH",
    "~": "TILDE",
    "*": "ASTERISK",
    "+": "PLUS",
    "(": "LEFT_PAREN",
    ")": "RIGHT_PAREN",
    "<": "LEFT_ANGLE_BRACKET",
    ">": "RIGHT_ANGLE_BRACKET",
    "{": "LEFT_CURLY_BRACE",
    "}": "RIGHT_CURLY_BRACE",
    "?": "QUESTION",
    ":": "COLON",
    "_": "UNDERSCORE",
    '"': "DOUBLE_QUOTE",
    "@": "AT",
    "#": "HASH",
    "$": "DOLLAR",
    "!": "EXCLAIM",
    "%": "PERCENT",
    "^": "CIRCUMFLEX",
    "&": "AMPERSAND",
    "|": "PIPE"
}
def expand_keycode_fnc(DEFINITION):
    if DEFINITION in alternate_keycodes:
        DEFINITION = alternate_keycodes[DEFINITION]
    
    if DEFINITION in [
        "A", "a", "B", "b", "C", "c", "D", "d", "E", "e",
        "F", "f", "G", "g", "H", "h", "I", "i", "J", "j",
        "K", "k", "L", "l", "M", "m", "N", "n", "O", "o",
        "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t",
        "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y",
        "Z", "z", "1", "2", "3", "4", "5", "6", "7", "8",
        "9", "0", "F1", "F2", "F3", "F4", "F5", "F6", "F7",
        "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15",
        "F16", "F17", "F18", "F19", "F20", "F21", "F22",
        "F23", "F24", "ENTER", "ENT", "ESCAPE", "ESC",
        "BSPACE", "BSPC", "TAB", "SPACE", "SPC", "NONUS_HASH",
        "NUHS", "NONUS_BSLASH", "NUBS", "COMMA", "COMM",
        "DOT", "SLASH", "SLSH", "TILDE", "TILD", "EXCLAIM",
        "EXLM", "AT", "HASH", "DOLLAR", "DLR", "PERCENT",
        "PERC", "CIRCUMFLEX", "CIRC", "AMPERSAND", "AMPR",
        "ASTERISK", "ASTR", "LEFT_PAREN", "LPRN", "RIGHT_PAREN",
        "RPRN", "UNDERSCORE", "UNDS", "PLUS", "LEFT_CURLY_BRACE",
        "LCBR", "RIGHT_CURLY_BRACE", "RCBR", "PIPE", "COLON",
        "COLN", "DOUBLE_QUOTE", "DQUO", "DQT",
        "LEFT_ANGLE_BRACKET", "LABK", "LT", "RIGHT_ANGLE_BRACKET",
        "RABK", "GT", "QUESTION", "QUES", "SCOLON", "SCLN",
        "QUOTE", "QUOT", "LBRACKET", "LBRC", "RBRACKET", "RBRC",
        "BSLASH", "BSLS", "MINUS", "MINS", "EQUAL", "EQL",
        "GRAVE", "GRV", "ZKHK", "CAPSLOCK", "CLCK", "CAPS",
        "SCROLLOCK", "SLCK", "BRMD", "NUMLOCK", "NLCK",
        "LOCKING_CAPS", "LCAP", "LOCKING_NUM", "LNUM",
        "LOCKING_SCROLL", "LSCR", "LCTRL", "LCTL", "LSHIFT",
        "LSFT", "LALT", "LGUI", "LCMD", "LWIN", "RCTRL",
        "RCTL", "RSHIFT", "RSFT", "RALT", "RGUI", "RCMD",
        "RWIN", "INT1", "RO", "INT2", "KANA", "INT3", "JYEN",
        "INT4", "HENK", "INT5", "MHEN", "INT6", "INT7",
        "INT8", "INT9", "LANG1", "HAEN", "LANG2", "HANJ",
        "LANG3", "LANG4", "LANG5", "LANG6", "LANG7", "LANG8",
        "LANG9", "PSCREEN", "PSCR", "PAUSE", "PAUS", "BRK",
        "BRMU", "INSERT", "INS", "HOME", "PGUP", "DELETE",
        "DEL", "END", "PGDOWN", "PGDN", "RIGHT", "RGHT",
        "LEFT", "DOWN", "UP", "APPLICATION", "APP", "POWER",
        "EXECUTE", "EXEC", "HELP", "MENU", "SELECT", "SLCT",
        "STOP", "AGAIN", "AGIN", "UNDO", "CUT", "COPY",
        "PASTE", "PSTE", "FIND", "MUTE", "VOLUP", "VOLDOWN",
        "ALT_ERASE", "ERAS", "SYSREQ", "CANCEL", "CLEAR",
        "CLR", "PRIOR", "RETURN", "SEPARATOR", "OUT", "OPER",
        "CLEAR_AGAIN", "CRSEL", "EXSEL", "SYSTEM_POWER",
        "PWR", "SYSTEM_SLEEP", "SLEP", "SYSTEM_WAKE", "WAKE",
        "AUDIO_MUTE", "MUTE", "AUDIO_VOL_UP", "VOLU",
        "AUDIO_VOL_DOWN", "VOLD", "MEDIA_NEXT_TRACK", "MNXT",
        "MEDIA_PREV_TRACK", "MPRV", "CPRV", "MEDIA_STOP", "MSTP",
        "MEDIA_PLAY_PAUSE", "MPLY", "MEDIA_SELECT", "MSEL",
        "MEDIA_EJECT", "EJCT", "MAIL", "CALCULATOR", "CALC",
        "MY_COMPUTER", "MYCM", "WWW_SEARCH", "WSCH", "WWW_HOME",
        "WHOM", "WWW_BACK", "WBAK", "WWW_FORWARD", "WFWD",
        "WWW_STOP", "WSTP", "WWW_REFRESH", "WREF",
        "WWW_FAVORITES", "WFAV", "MEDIA_FAST_FORWARD", "MFFD",
        "MEDIA_REWIND", "MRWD", "BRIGHTNESS_UP", "BRIU",
        "BRIGHTNESS_DOWN", "BRID", "KP_SLASH", "PSLS",
        "KP_ASTERISK", "PAST", "KP_MINUS", "PMNS", "KP_PLUS",
        "PPLS", "KP_ENTER", "PENT", "KP_1", "P1", "KP_2", "P2",
        "KP_3", "P3", "KP_4", "P4", "KP_5", "P5", "KP_6", "P6",
        "KP_7", "P7", "KP_8", "P8", "KP_9", "P9", "KP_0", "P0",
        "KP_DOT", "PDOT", "KP_EQUAL", "PEQL", "KP_COMMA", "PCMM",
        "MS_BTN1", "BTN1", "MS_BTN2", "BTN2", "MS_BTN3", "BTN3",
        "MS_BTN4", "BTN4", "MS_BTN5", "BTN5", "MS_BTN6", "BTN6",
        "MS_LEFT", "MS_L", "MS_DOWN", "MS_D", "MS_UP", "MS_U",
        "MS_RIGHT", "MS_R", "MS_WH_UP", "WH_U", "MS_WH_DOWN",
        "WH_D", "MS_WH_LEFT", "MS_WH_L", "MS_WH_RIGHT", "MS_WH_R",
        "MS_ACCEL0", "ACL0", "MS_ACCEL1", "ACL1", "MS_ACCEL2", "ACL2"
        ]:
        return "KC_" + DEFINITION
    else:
        return DEFINITION

def MK(on_pseudolayer, keycodes_hash, definition, output_buffer, index):
    output_buffer += stitch(
        "void function_{}(const struct Chord* self) {{".format(index),
        "    switch (*self->state) {",
        "        case ACTIVATED:",
        stitch(
            "            key_in({});".format(expand_keycode_fnc(val)) for val in definition.split(','),
            "            break;",
            "        case DEACTIVATED:"
        ),
        reduce(newline_separator, ["            key_out({});".format(expand_keycode_fnc(val)) for val in definition.split(',')]),
        "            *self->state = IDLE;",
        "            break;",
        "        case RESTART:",
        reduce(newline_separator, ["            key_out({});".format(expand_keycode_fnc(val)) for val in definition.split(',')]),
        "            break;",
        "        default:",
        "            break;",
        "    };",
        "}",
        "",
        my_format(S = chord_with_counter,
            index = index,
            on_pseudolayer = on_pseudolayer,
            keycodes_hash = keycodes_hash,
            value1 = 0, 
            value2 = 0,
            function = "function_" + str(index))
    )
    
    return [output_buffer, index+1]

def D(on_pseudolayer, keycodes_hash, DEFINITION, output_buffer, index):
    output_buffer += stitch(
        stitch(
            "void function_{}(const struct Chord* self) {{".format(index),
            "    switch (*self->state) {",
            "        case ACTIVATED:",
            "            *self->counter = *self->counter + 1;",
            "            break;",
            "        case PRESS_FROM_ACTIVE:",
            "            switch (*self->counter) {",
        ),
        "",
        stitch(
            reduce(newline_separator, [
                "                case {}:".format(i+1),
                "                    key_in({});".format(expand_keycode_fnc(val.strip())),
                "                    break;"
            ]) for i, val in enumerate(DEFINITION.split(','))
        ),
        "",
        stitch(
            "                default:",
            "                    break;",
            "            }",
            "            *self->state = FINISHED_FROM_ACTIVE;",
            "            break;",
            "        case FINISHED:",
            "            switch (*self->counter) {",
        ),
        "",
        stitch(
            reduce(newline_separator, [
                "                case {}:".format(i+1),
                "                    tap_key( {});".format(expand_keycode_fnc(val)),
                "                    break;"
            ]) for i, val in enumerate(DEFINITION.split(','))
        ),
        "",
        stitch(
            "                default:",
            "                    break;",
            "            }",
            "            *self->counter = 0;",
            "            *self->state = IDLE;",
            "            break;",
            "        case RESTART:",
            "            switch (*self->counter) {",
        ),
        "",
        stitch(
            reduce(newline_separator, [
                "                case {}:".format(i + 1),
                "                    key_out({});".format(expand_keycode_fnc(val)),
                "                    break;"
            ]) for i, val in enumerate(DEFINITION.split(','))
        ),
        "",
        stitch(
            "                default:",
            "                    break;",
            "            }",
            "            *self->counter = 0;",
            "            break;",
            "        default:",
            "            break;",
            "    }",
            "}",
        ),
        "",
        my_format(S = chord_with_counter,
            index = index,
            on_pseudolayer = on_pseudolayer,
            keycodes_hash = keycodes_hash,
            value1 = 0, 
            value2 = 0,
            function = "function_" + str(index))
    )

    return [output_buffer, index+1]

def O(on_pseudolayer, keycodes_hash, DEFINITION, output_buffer, index):
    if DEFINITION[0:3] == "KC_":
        return OSK(on_pseudolayer, keycodes_hash, DEFINITION, output_buffer, index)
    else:
        return OSL(on_pseudolayer, keycodes_hash, DEFINITION, output_buffer, index)

def add_key(PSEUDOLAYER, KEYCODES_HASH, DEFINITION, output_buffer, index, number_of_strings, strings):
    # if "= {" + KEYCODES_HASH + ", " + PSEUDOLAYER in output_buffer:
    #     KEYCODES_HASH = re.sub('H_', '', KEYCODES_HASH)
    #     raise Exception("You are trying to register a chord that you already registered (" + KEYCODES_HASH + ", " + PSEUDOLAYER + ")")
    
    if DEFINITION == "":
        return [output_buffer, index, number_of_strings, strings]
    else:
        split = DEFINITION.split("(")
        type = split[0].strip()
        if len(split) == 1:
            if type == "LOCK":
                [output_buffer, index] = LOCK(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            elif type == "AT":
                [output_buffer, index] = AT(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            elif type == "CMD":
                [output_buffer, index] = CMD(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            elif type == "LEAD":
                [output_buffer, index] = LEAD(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            elif type == "DM_RECORD":
                [output_buffer, index] = DM_RECORD(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            elif type == "DM_NEXT":
                [output_buffer, index] = DM_NEXT(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            elif type == "DM_END":
                [output_buffer, index] = DM_END(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            elif type == "DM_PLAY":
                [output_buffer, index] = DM_PLAY(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            elif type == "CLEAR_KB":
                [output_buffer, index] = CLEAR(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            elif type == "RESET":
                [output_buffer, index] = RESET(PSEUDOLAYER, KEYCODES_HASH, output_buffer, index)
            else:
                code = expand_keycode_fnc(type)
                output_buffer += my_format(s = KC, on_pseudolayer = PSEUDOLAYER, keycodes_hash = KEYCODES_HASH, keycode = code, index = index) + '\n'
                index = index + 1
        else:
            val = split[1][:-1].strip()
            if type == "O":
                code = expand_keycode_fnc(val)
                [output_buffer, index] = O(PSEUDOLAYER, KEYCODES_HASH, code, output_buffer, index)
            elif type == "D":
                [output_buffer, index] = D(PSEUDOLAYER, KEYCODES_HASH, val, output_buffer, index)
            elif type == "MK":
                [output_buffer, index] = MK(PSEUDOLAYER, KEYCODES_HASH, val, output_buffer, index)
            elif type == "M":
                fnc = val.split(',')[0].strip()
                val1 = val.split(',')[1].strip()
                val2 = val.split(',')[2].strip()
                [output_buffer, index] = M(PSEUDOLAYER, KEYCODES_HASH, val1, val2, fnc, output_buffer, index)
            elif type == "KK":
                val1 = val.split(',')[0].strip()
                code1 = expand_keycode_fnc(val1)
                val2 = val.split(',')[1].strip()
                code2 = expand_keycode_fnc(val2)
                [output_buffer, index] = KK(PSEUDOLAYER, KEYCODES_HASH, code1, code2, output_buffer, index)
            elif type == "KL":
                val1 = val.split(',')[0].strip()
                code1 = expand_keycode_fnc(val1)
                val2 = val.split(',')[1].strip()
                [output_buffer, index] = KL(PSEUDOLAYER, KEYCODES_HASH, code1, val2, output_buffer, index)
            elif type == "KM":
                val1 = val.split(',')[0].strip()
                code1 = expand_keycode_fnc(val1)
                val2 = val.split(',')[1].strip()
                code2 = expand_keycode_fnc(val2)
                [output_buffer, index] = KM(PSEUDOLAYER, KEYCODES_HASH, code1, code2, output_buffer, index)
            elif type == "AS":
                code = expand_keycode_fnc(val)
                [output_buffer, index] = AS(PSEUDOLAYER, KEYCODES_HASH, code, output_buffer, index)
            elif type == "MO":
                if not ',' in val:
                    [output_buffer, index] = MO(PSEUDOLAYER, KEYCODES_HASH, val, output_buffer, index)
                else:
                    val1 = val.split(',')[0].strip()
                    val2 = val.split(',')[1].strip()
                    [output_buffer, index] = MO_alt(PSEUDOLAYER, KEYCODES_HASH, val1, val2, output_buffer, index)
            elif type == "DF":
                [output_buffer, index] = DF(PSEUDOLAYER, KEYCODES_HASH, val, output_buffer, index)
            elif type == "TO":
                [output_buffer, index] = TO(PSEUDOLAYER, KEYCODES_HASH, val, output_buffer, index)
            elif type == "STR":
                [output_buffer, index, number_of_strings, strings] = STR(PSEUDOLAYER, KEYCODES_HASH, val, output_buffer, index, number_of_strings, strings)
    return [output_buffer, index, number_of_strings, strings]

#def add_leader_combo(DEFINITION, FUNCTION):
#    return list_of_leader_combos.append([DEFINITION, FUNCTION])

def add_chord_set(PSEUDOLAYER, INPUT_STRING, TYPE, data, output_buffer, index, number_of_strings, strings):
    chord_set = {}
    for set in data["chord_sets"]:
        if set["name"] == TYPE:
            chord_set = set["chords"]
            break
    
    separated_string = top_level_split(INPUT_STRING)
    for word, chord in zip(separated_string, chord_set):
        chord_hash = reduce((lambda x, y: str(x) + " + " + str(y)), ["H_" + key for key in chord])
        [output_buffer, index, number_of_strings, strings] = add_key(PSEUDOLAYER, chord_hash, word, output_buffer, index, number_of_strings, strings)
    
    return [output_buffer, index, number_of_strings, strings]

def add_dictionary(PSEUDOLAYER, keycodes, array, output_buffer, index, number_of_strings, strings):
    for chord in array:
        hash = ""
        for word, key in zip(chord[:-1], keycodes):
            if word == "X":
                hash = hash + " + H_" + key
        hash = hash[3:]
        if hash != "":
            [output_buffer, index, number_of_strings, strings] = add_key(PSEUDOLAYER, hash, chord[-1], output_buffer, index, number_of_strings, strings)
    
    return [output_buffer, index, number_of_strings, strings]

def secret_chord(PSEUDOLAYER, ACTION, INPUT_STRING, data, output_buffer, index, number_of_strings, strings):
    separated_string = top_level_split(INPUT_STRING)
    hash = ""
    for word, key in zip(separated_string, data["keys"]):
        if word == "X":
            hash = hash + " + H_" + key
    
    hash = hash[3:]
    if hash != "":
        return add_key(PSEUDOLAYER, hash, ACTION, output_buffer, index, number_of_strings, strings)