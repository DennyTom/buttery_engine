alternate_short_keycodes = {
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
    "@": "KC_AT",
    "#": "HASH",
    "$": "DOLLAR",
    "!": "EXCLAIM",
    "%": "PERCENT",
    "^": "CIRCUMFLEX",
    "&": "AMPERSAND",
    "|": "PIPE"
}

supported_short_keycodes = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "TILDE", "TILD", "EXCLAIM", "EXLM", "HASH", "DOLLAR", "DLR", "PERCENT", "PERC", "CIRCUMFLEX", "CIRC", "AMPERSAND", "AMPR", "ASTERISK", "ASTR", "LEFT_PAREN", "LPRN", "RIGHT_PAREN", "RPRN", "UNDERSCORE", "UNDS", "PLUS",
    "LEFT_CURLY_BRACE", "LCBR", "RIGHT_CURLY_BRACE", "RCBR", "PIPE", "COLON", "COLN", "DOUBLE_QUOTE", "DQUO", "DQT", "LEFT_ANGLE_BRACKET", "LABK", "LT", "RIGHT_ANGLE_BRACKET", "RABK", "GT", "QUESTION", "QUES", "SCOLON", "SCLN", "QUOTE", "QUOT", "LBRACKET", "LBRC", "RBRACKET", "RBRC", "BSLASH", "BSLS", "MINUS", "MINS", "EQUAL", "EQL", "GRAVE", "GRV","ZKHK",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F19", "F20", "F21", "F22", "F23", "F24",
    "ENTER", "ENT", "ESCAPE", "ESC", "BSPACE", "BSPC", "TAB", "SPACE", "SPC", "NONUS_HASH", "NUHS", "NONUS_BSLASH", "NUBS", "COMMA", "COMM", "DOT", "SLASH", "SLSH",
    "CAPSLOCK", "CLCK", "CAPS", "SCROLLOCK", "SLCK", "BRMD", "NUMLOCK", "NLCK", "LOCKING_CAPS", "LCAP", "LOCKING_NUM", "LNUM", "LOCKING_SCROLL", "LSCR",
    "LCTRL", "LCTL", "LSHIFT", "LSFT", "LALT", "LGUI", "LCMD", "LWIN", "RCTRL", "RCTL", "RSHIFT", "RSFT", "RALT", "RGUI", "RCMD", "RWIN",
    "INT1", "RO", "INT2", "KANA", "INT3", "JYEN", "INT4", "HENK", "INT5", "MHEN", "INT6", "INT7", "INT8", "INT9", "LANG1", "HAEN", "LANG2", "HANJ", "LANG3", "LANG4", "LANG5", "LANG6", "LANG7", "LANG8", "LANG9",
    "PSCREEN", "PSCR", "PAUSE", "PAUS", "BRK", "BRMU", "INSERT", "INS", "HOME", "PGUP", "DELETE", "DEL", "END", "PGDOWN", "PGDN", "RIGHT", "RGHT", "LEFT", "DOWN", "UP", "APPLICATION", "APP", "POWER", "EXECUTE", "EXEC", "HELP", "MENU", "SELECT", "SLCT", "STOP", "AGAIN", "AGIN", "UNDO", "CUT", "COPY", "PASTE", "PSTE", "FIND", "MUTE", "VOLUP", "VOLDOWN", "ALT_ERASE", "ERAS", "SYSREQ", "CANCEL", "CLEAR", "CLR", "PRIOR", "RETURN", "SEPARATOR", "OUT", "OPER", "CLEAR_AGAIN", "CRSEL", "EXSEL",
    "SYSTEM_POWER", "PWR", "SYSTEM_SLEEP", "SLEP", "SYSTEM_WAKE", "WAKE", "AUDIO_MUTE", "MUTE", "AUDIO_VOL_UP", "VOLU", "AUDIO_VOL_DOWN", "VOLD", "MEDIA_NEXT_TRACK", "MNXT", "MEDIA_PREV_TRACK", "MPRV", "CPRV", "MEDIA_STOP", "MSTP", "MEDIA_PLAY_PAUSE", "MPLY", "MEDIA_SELECT", "MSEL", "MEDIA_EJECT", "EJCT", "MAIL", "CALCULATOR", "CALC", "MY_COMPUTER", "MYCM", "WWW_SEARCH", "WSCH", "WWW_HOME", "WHOM", "WWW_BACK", "WBAK", "WWW_FORWARD", "WFWD", "WWW_STOP", "WSTP", "WWW_REFRESH", "WREF", "WWW_FAVORITES", "WFAV",  "MEDIA_FAST_FORWARD", "MFFD", "MEDIA_REWIND", "MRWD", "BRIGHTNESS_UP", "BRIU", "BRIGHTNESS_DOWN", "BRID",
    "KP_SLASH", "PSLS", "KP_ASTERISK", "PAST", "KP_MINUS", "PMNS", "KP_PLUS", "PPLS", "KP_ENTER", "PENT", "KP_1", "P1", "KP_2", "P2", "KP_3", "P3", "KP_4", "P4", "KP_5", "P5", "KP_6", "P6", "KP_7", "P7", "KP_8", "P8", "KP_9", "P9", "KP_0", "P0", "KP_DOT", "PDOT", "KP_EQUAL", "PEQL", "KP_COMMA", "PCMM",
    "MS_BTN1", "BTN1", "MS_BTN2", "BTN2", "MS_BTN3", "BTN3", "MS_BTN4", "BTN4", "MS_BTN5", "BTN5", "MS_BTN6", "BTN6", "MS_LEFT", "MS_L", "MS_DOWN", "MS_D", "MS_UP", "MS_U", "MS_RIGHT", "MS_R", "MS_WH_UP", "WH_U", "MS_WH_DOWN", "WH_D", "MS_WH_LEFT", "MS_WH_L", "MS_WH_RIGHT", "MS_WH_R", "MS_ACCEL0", "ACL0", "MS_ACCEL1", "ACL1", "MS_ACCEL2", "ACL2" 
]

def expand_keycode(keycode):
    keycode = keycode.upper()

    if keycode in alternate_short_keycodes:
        keycode = alternate_short_keycodes[keycode]

    if keycode in supported_short_keycodes:
        return f"KC_{keycode}"
    else:
        return keycode