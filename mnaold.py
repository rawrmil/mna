#!/bin/python3

import sys
import sympy as sp
from sympy.parsing.mathematica import parse_mathematica
import json

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
            "properties": json.loads(tokens[2])
        })
        props = circuit[-1]["properties"]
        for k, v in props.items():
             props[k] = parse_mathematica(str(v))
    return circuit

def AddElementToEquation(e, epot, ecur, upot, ucur):
    name = e["name"]
    etype = e["type"]
    nodes = e["nodes"]
    props = e["properties"]
    if etype == "r":
        pot1, pot2 = upot[nodes[0]], upot[nodes[1]]
        r = props["r"]
        epot[nodes[0]] += (pot1-pot2)/r
        epot[nodes[1]] -= (pot1-pot2)/r
    elif etype == "cs":
        i = props["i"]
        epot[nodes[0]] += i
        epot[nodes[1]] -= i
    elif etype == "vs":
        u = props["u"]
        pot1, pot2 = upot[nodes[0]], upot[nodes[1]]
        epot[nodes[0]] += ucur[name]
        epot[nodes[1]] -= ucur[name]
        ecur[name] += pot2-pot1-u

# S O L V E

def SolveForVoltageAndCurrent(e, upot, ucur, sol):
    name = e["name"]
    etype = e["type"]
    nodes = e["nodes"]
    props = e["properties"]
    pot1, pot2 = upot[nodes[0]], upot[nodes[1]]
    if etype == "r":
        props["u"] = (pot1-pot2).subs(sol)
        props["i"] = (props["u"]/props["r"]).subs(sol)
    elif etype == "cs":
        props["u"] = (pot2-pot1).subs(sol)
    elif etype == "vs":
        props["i"] = (ucur[name]).subs(sol)
    

def Solve(circuit):
    # Defining unknowns (potentials & currents)
    upot = dict()
    ucur = dict()
    for e in circuit:
        if e["type"] == "vs":
            name = e["name"]
            ucur[name] = sp.Symbol(f"i_{name}", complex=True)
        for name in e["nodes"]:
            upot[name] = sp.Symbol(f"p_{name}", complex=True)
    gnd = list(upot.values())[-1]
    # Equations
    epot = dict((u, 0) for u in upot)
    ecur = dict((u, 0) for u in ucur)
    for e in circuit:
        AddElementToEquation(e, epot, ecur, upot, ucur)
    # Solving
    elist = list(epot.values())+list(ecur.values())+[gnd]
    ulist = list(upot.values())+list(ucur.values())
    sol = sp.solve(elist, ulist)
    # Finding voltages & currents
    for e in circuit:
        SolveForVoltageAndCurrent(e, upot, ucur, sol)
    return circuit

# M A I N

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Not enough arguments")
        exit(1)
    circuit = Parse(sys.argv[1])
    Solve(circuit)
    for e in circuit:
        name = e["name"]
        props = e["properties"]
        print(f"u_{name} = {sp.simplify(props['u'])}")
        print(f"i_{name} = {sp.simplify(props['i'])}")
