#!/usr/bin/python3

import re
import sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations
from typing import List

"""
INPUT:

./mna.py [-complex] node1 node2 type_name expr; ...

CONSTRAINTS:

node: a-zA-Z0-9
type: i/I, u/U, r/R
name: a-zA-Z0-9
expr: ???
"""

# S T A T E

is_complex=False

# E R R O R

def Error(name):
    sys.stderr.write(name)
    exit(1)

# P A R S E

def ProcessElementProperties(prop):
    name_pattern = re.compile("^[a-zA-Z0-9_-]*$")
    if len(prop) < 4:
        Error("parse-argument-shortage")
    if not name_pattern.match(prop[0]):
        Error("parse-pattern-node-src")
    if not name_pattern.match(prop[1]):
        Error("parse-pattern-node-dst")
    prop[2] = prop[2].split("_", 1)
    if len(prop[2]) != 2:
        Error("parse-name-type-separator")
    if prop[2][0] == '':
        Error("parse-empty-type")
    if prop[2][1] == '':
        Error("parse-empty-name")
    if not name_pattern.match(prop[2][1]):
        Error("parse-pattern-name")
    if not prop[2][0].lower() in ['i', 'u', 'r']:
        Error("parse-no-such-etype")
    prop[3] = parse_expr(prop[3])
    if is_complex:
        syms = prop[3].free_symbols
        complex_syms = {s: symbols(s.name, complex=True) for s in syms}
        prop[3] = expr.subs(complex_syms)

def ParseCircuit(text: str):
    prop_list = [e.strip().split(None, 3) for e in text.split(';')]
    for i, p in enumerate(prop_list):
        ProcessElementProperties(p)
    print(prop_list)

# S O L V E

def Solve(circuit):
    pass

if __name__ == "__main__":
    if len(sys.argv) == 1:
        exit(1)
    if "-complex" in sys.argv:
        is_complex=True
        sys.argv.delete("-complex")
    circuit = ParseCircuit(" ".join(sys.argv[1:]))
    Solve(circuit)
