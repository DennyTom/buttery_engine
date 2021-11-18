#!/usr/bin/env python3

import argparse
import engine.keycodes

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
    print(args.input)

    
