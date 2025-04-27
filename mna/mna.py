#!/usr/bin/python3

# TODO: Strict typing

import sys
import yaml
import sympy as sp
from sympy.parsing.mathematica import parse_mathematica

# P A R S I N G

def ParseVariable(var, local_vars):
    # TODO: Check if name is right
    # TODO: Check if name is unique
    # TODO: Check if type is right
    name = var["name"]
    _real = True if var["type"] == "real" else None
    _complex = True if var["type"] == "complex" else None
    local_vars[name] = sp.Symbol(name, real=_real, complex=_complex)

def ParseElement(elem, local_vars):
    # TODO: Check if all variables are in local_vars
    # TODO: Check if value is a string or a number
    # TODO: Check if nodes is str/integer
    elem["nodes"] = [str(node) for node in elem["nodes"]]
    parameters = elem["parameters"]
    for param in parameters.items():
        key, value = param
        value = str(value)
        parameters[key] = parse_mathematica(value)
        replacement_dict = { sp.Symbol(k): v for k, v in local_vars.items() }
        parameters[key] = parameters[key].subs(replacement_dict)


def Parse(fname):
    # TODO: Structural checks
    circuit_file = open(sys.argv[1], "r")
    circuit_data = yaml.safe_load(circuit_file)
    circuit_file.close()
    circuit = circuit_data["circuit"]
    # Parse variables
    variables = circuit["variables"]
    local_vars = {}
    for var in variables:
        ParseVariable(var, local_vars)
    # Parse elements
    elements = circuit["elements"]
    for elem in elements:
        ParseElement(elem, local_vars)
    return circuit_data

# S O L V I N G

def AddElementToEquations(elem, equations, unknowns):
    etype = elem["type"]
    nodes = elem["nodes"]
    parameters = elem["parameters"]
    if etype == "resistor":
        pot1, pot2 = unknowns[nodes[0]], unknowns[nodes[1]]
        equations[nodes[0]] += ((pot1-pot2)/parameters["resistance"])
        equations[nodes[1]] -= ((pot2-pot1)/parameters["resistance"])
    elif etype == "current_source":
        equations[nodes[0]] -= parameters["current"]
        equations[nodes[1]] += parameters["current"]
    elif etype == "voltage_source":
        pot1, pot2 = unknowns[nodes[0]], unknowns[nodes[1]]
        equations[nodes[0]] += unknowns[elem["name"]]
        equations[nodes[1]] -= unknowns[elem["name"]]
        equations[elem["name"]] += pot1-pot2+parameters["voltage"]

def Solve(circuit_data):
    circuit = circuit_data["circuit"]
    elements = circuit["elements"]
    # Creating node list
    unknowns = dict()
    gnd_potential = None
    for elem in elements:
        if elem["type"] == "voltage_source":
            name = elem["name"]
            unknowns[name] = sp.Symbol(f"i_{name}", complex=True)
        for name in elem["nodes"]:
            unknowns[name] = sp.Symbol(f"p_{name}", complex=True)
            gnd_potential = unknowns[name]
    # Equation System
    equations = dict((v, 0) for v in unknowns)
    for elem in elements:
        AddElementToEquations(elem, equations, unknowns)
    equations["GND"] = gnd_potential
    print(" = 0\n".join([f"{e[0]}: {e[1]}" for e in equations.items()]), end=" = 0\n")
    # Solving for unknowns
    equations_list = list(equations.values())
    unknowns_list = list(unknowns.values())
    sol = sp.solve(equations_list, unknowns_list)
    print("unknowns:", unknowns.values())
    print("solution:", sol)

# M A I N

if __name__ == "__main__":
    if len(sys.argv) != 2:
        # TODO: Error handling
        print("pipenv run ./mna.py [file]")
        exit(1)
    circuit_data = Parse(sys.argv[1])
    Solve(circuit_data)
