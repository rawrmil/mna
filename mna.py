#!/bin/python3

import sys
import json

# 1-2 V2_1 {...}; ...
def Parse(text):
    # Skipping dicts and splitting by ';' or '\n'
    sectors = [""]
    curly_depth = 0
    single_quotes_flag = False
    double_quotes_flag = False
    for i, c in enumerate(text):
        quotes_flag = (single_quotes_flag or double_quotes_flag)
        if quotes_flag and curly_depth == 0:
            # TODO: Quotes out of dict
            exit(1)
        if not single_quotes_flag and c == '"':
            double_quotes_flag = not double_quotes_flag
        elif not double_quotes_flag and c == "'":
            single_quotes_flag = not single_quotes_flag
        elif not quotes_flag and c == "{":
            curly_depth += 1
        elif not quotes_flag and c == "}":
            curly_depth -= 1
        elif curly_depth == 0 and c in [";", "\n"]:
            sectors.append("")
            continue
        sectors[-1] += c
    # Creating circuit
    circuit = []
    for e in sectors:
        tokens = e.strip().split(maxsplit=3)
        print(tokens)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        # TODO: Not enough arguments
        exit(1)
    circuit = Parse(sys.argv[1])
    print(circuit)
