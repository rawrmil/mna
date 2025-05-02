#!/bin/python3

import sys
import sympy as sp
from pyhocon import ConfigFactory

# TODO: Error handling when string parsing

# P A R S E

def Parse(text):
    # Skipping dicts and splitting by ';' or '\n'
    sectors = [""]
    curly_depth = 0
    single_quotes_flag = False
    double_quotes_flag = False
    for i, c in enumerate(text):
        quotes_flag = (single_quotes_flag or double_quotes_flag)
        if quotes_flag and curly_depth == 0:
            print("Quotes out of dict")
            exit(1)
        if not single_quotes_flag and c == '"':
            double_quotes_flag = not double_quotes_flag
        elif not double_quotes_flag and c == "'":
            single_quotes_flag = not single_quotes_flag
        elif not quotes_flag and c == "{":
            curly_depth += 1
        elif not quotes_flag and c == "}":
            curly_depth -= 1
            if curly_depth < 0:
                print(f"Unexpected '{'}'}' at {i}")
                exit(1)
        elif curly_depth == 0 and c == ";":
            sectors.append("")
            continue
        sectors[-1] += c
    # Creating circuit
    circuit = []
    for e in sectors:
        tokens = e.strip().split(maxsplit=2)
        if len(tokens) != 3:
            print("Two whitespaces needed in each element")
            exit(1)
        nodes = tokens[0].split('-')
        etype, name = tokens[1].split('_')
        circuit.append({
            "nodes": nodes,
            "type": etype.lower(),
            "name": name,
            "properties": dict(ConfigFactory.parse_string(tokens[2]))
        })
    return circuit

# P A R S E

def Solve(circuit):
    # Defining unknowns (node potentials & VS currents)
    unknowns = dict()
    gnd_potential = None
    for elem in circuit:
        print(elem["type"])
        if elem["type"] == "vs":
            name = elem["name"]
            unknowns[name] = sp.Symbol(f"i_{name}", complex=True)
        for name in elem["nodes"]:
            unknowns[name] = sp.Symbol(f"p_{name}", complex=True)
            gnd_potential = unknowns[name]
    print("unknowns:", unknowns)

# M A I N

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Not enough arguments")
        exit(1)
    circuit = Parse(sys.argv[1])
    Solve(circuit)
