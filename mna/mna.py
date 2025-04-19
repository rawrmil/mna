#!/usr/bin/python3

import re
import sys
import sympy as sp
from typing import List

"""
INPUT:

./mna.py node1 node2 type_name expr; ...

CONSTRAINTS:

node: a-zA-Z0-9
type: i/I, u/U, r/R
name: a-zA-Z0-9
value: float
expr: ???
"""

# C L A S S E S

class Element:
    def __init__(self, node1: str, node2: str, etype: str, name: str, value: sp.Expr):
        self.node1 = node1
        self.node2 = node2
        self.etype = etype
        self.name = name
        self.value = sp.Expr()
        self.voltage = sp.Expr()
        self.current = sp.Expr()

class Circuit:

    def __init__(self, text: str):
        self.elements = []
        self.ParseCircuit(text)
        
    # P A R S E

    def ProcessElementProperties(self, index: int, prop):
        name_pattern = re.compile("^[a-zA-Z0-9_-]*$")
        if len(prop) < 4:
            sys.stderr.write("argument-shortage")
        if len(prop) > 4:
            sys.stderr.write("argument-overage")
        if not name_pattern.match(prop[0]):
            sys.stderr.write("pattern-node-src")
        if not node_pattern.match(prop[1]):
            sys.stderr.write("pattern-node-dst")
        prop[2] = prop[2].split("_", 1)
        if len(prop[2]) == 1:
            sys.stderr.write("name-type-separator")
        if prop[2][0] == '':
            sys.stderr.write("empty-type")
        if prop[2][1] == '':
            sys.stderr.write("empty-name")
        if not name_pattern.match(prop[2][1]):
            sys.stderr.write("pattern-name")
        if not prpp[2][0].lower() in ['i', 'u', 'r']:
            sys.stderr.write("no-such-etype")
        self.elements.append(
            Element(
                node1=prop[0],
                node2=prop[1],
                etype=prop[2],
                value=prop[3]
            )
        )

    def ParseCircuit(self, text: str):
        prop_list = [e.strip().split() for e in text.split(';')]
        for i, p in enumerate(prop_list):
            self.ProcessElementProperties(i, p)

    # S O L V E

    def Solve(self):
        pass



if __name__ == "__main__":
    if len(sys.argv) == 1:
        exit(1)
    text = " ".join(sys.argv[1:])
    circuit = Circuit(text)
    circuit.Solve()
