#!/usr/bin/env python3

import argparse
import engine.keycodes
from engine.parser import buttery_parser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Parse Buttery Engine JSON definition to a QMK compatible keymap"
    )
    parser.add_argument(
        "input",
        metavar = "input",
        type = str,
        help = "Path to the input JSON"
    )
    args = parser.parse_args()

    with open('engine/template.txt', 'r') as file:
        template = file.read()

    includes, keycodes, pseudolayers, keyboard_parameters, keymaps, buffers, chords = buttery_parser(args.input)

    keymap = template.format(
        includes = includes,
        keycodes = keycodes,
        pseudolayers = pseudolayers,
        keyboard_parameters = keyboard_parameters,
        keymaps = keymaps,
        buffers = buffers,
        chords = chords
    )

    with open('keymap.c', 'w') as file:
        file.write(keymap)
