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

#def AddElementToEquations(elem, equations, unknown_variables):
#    etype = elem["type"]
#    nodes = elem["nodes"]
#    if etype == "resistor":
#        pos, neg = unknown_variables[nodes[0]], unknown_variables[nodes[1]]
#        equations[nodes[0]] = ((pos-neg)/elem["resistance"])
#        equations[nodes[1]] = ((neg-pos)/elem["resistance"])
#    elif etype == "current_source":
#        equations[nodes[0]] = -elem["current"]
#        equations[nodes[1]] = +elem["current"]
#    elif etype == "voltage_source":
#        current_name = f"i_{elem['name']}"
#        unknown_variables[current_name] = sp.Symbol(current_name, complex=True)
#        equations[nodes[0]] = +unknown_variables[-1]
#        equations[nodes[1]] = -unknown_variables[-1]

def Solve(circuit_data):
    circuit = circuit_data["circuit"]
    elements = circuit["elements"]
    # Creating node list
    unknown_variables = dict()
    for elem in elements:
        if elem["type"] == "voltage_source":
            name = elem["name"]
            unknown_variables[name] = sp.Symbol(f"i_{name}", complex=True)
        for name in elem["nodes"]:
            unknown_variables[name] = sp.Symbol(f"p_{name}", complex=True)
    print(unknown_variables)
    # Equation System
    #equations = dict((v, 0) for v in unknown_variables)
    #for elem in elements:
    #    AddElementToEquations(elem, equations, unknown_variables)
    #print(*equations, end="\n")

# M A I N

if __name__ == "__main__":
    if len(sys.argv) != 2:
        # TODO: Error handling
        print("pipenv run ./mna.py [file]")
        exit(1)
    circuit_data = Parse(sys.argv[1])
    Solve(circuit_data)
