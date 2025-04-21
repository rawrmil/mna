#!/usr/bin/python3

import re
import sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations
from typing import List

"""
INPUT:

./mna.py node1 node2 type_name expr; ...

CONSTRAINTS:

node: a-zA-Z0-9
type: i/I, u/U, r/R
name: a-zA-Z0-9
expr: ???
"""

# E R R O R

def Error(name):
    sys.stderr.write(name)
    print()
    exit(1)

# P A R S E

def ProcessElementProperties(element):
    name_pattern = re.compile("^[a-zA-Z0-9_-]*$")
    if len(element) < 4:
        Error("parse-argument-shortage")
    if not name_pattern.match(element[0]):
        Error("parse-pattern-node-src")
    if not name_pattern.match(element[1]):
        Error("parse-pattern-node-dst")
    element[2] = element[2].split("_", 1)
    if len(element[2]) != 2:
        Error("parse-name-type-separator")
    if element[2][0] == '':
        Error("parse-empty-type")
    if element[2][1] == '':
        Error("parse-empty-name")
    if not name_pattern.match(element[2][1]):
        Error("parse-pattern-name")
    if not element[2][0].lower() in ['i', 'u', 'r']:
        Error("parse-no-such-etype")
    element[3] = parse_expr(element[3])

def ParseCircuit(text: str):
    # TODO: Unique name check
    # TODO: Eq parse check
    prop_list = [e.strip().split(None, 3) for e in text.split(';')]
    for i, e in enumerate(prop_list):
        ProcessElementProperties(e)
    return prop_list

# S O L V E

def Solve(circuit):
    unique_nodes = set()
    for e in circuit:
        unique_nodes.add(e[0])
        unique_nodes.add(e[1])
    unique_nodes = sorted(unique_nodes)
    potentials = [sp.Symbol(f"p_{n}") for n in unique_nodes]
    unknown_currents = []
    eq_list = [0]*len(unique_nodes)
    for e in circuit:
        etype = e[2][0].lower()
        node1 = unique_nodes.index(e[0])
        node2 = unique_nodes.index(e[1])
        if etype == "r":
            eq_list[node1] += (potentials[node1]-potentials[node2])/e[3]
            eq_list[node2] += (potentials[node2]-potentials[node1])/e[3]
        if etype == "i":
            eq_list[node1] -= e[3]
            eq_list[node2] += e[3]
        if etype == "u":
            unknown_currents.append(sp.Symbol(f"i_{e[2][1]}"))
            eq_list[node1] += unknown_currents[-1]
            eq_list[node2] -= unknown_currents[-1]
            eq_list.append(potentials[node1]-potentials[node2]+e[3])
    eq_list.append(potentials[-1])
    print(eq_list)
    sol = sp.solve(eq_list, potentials+unknown_currents)
    print(sol)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        exit(1)
    circuit = ParseCircuit(" ".join(sys.argv[1:]))
    Solve(circuit)
