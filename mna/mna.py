#!/usr/bin/python3

# TODO: Strict typing

import sys
import yaml
import sympy as sp
from sympy.parsing.mathematica import parse_mathematica

def ParseVariable(var, local_vars):
    # TODO: Check if name is right
    # TODO: Check if name is unique
    name = var["name"]
    value = sp.Symbol(name)
    local_vars[name] = value

def ParseElement(elem, local_vars):
    parameters = elem["parameters"]
    # TODO: Check if all variables are in local_vars
    # TODO: Check if value is a string or a number
    for param in parameters.items():
        key, value = param
        value = str(value)
        parameters[key] = parse_mathematica(value)
        replacement_dict = { sp.Symbol(k): v for k, v in local_vars.items() }
        parameters[key] = parameters[key].subs(replacement_dict)
    print(f"elem: {elem}")


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
    print(variables)
    print(local_vars)
    # Parse elements
    elements = circuit["elements"]
    for elem in elements:
        ParseElement(elem, local_vars)
    return circuit_data

def Solve(circuit):
    pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        # TODO: Erro handling
        print("pipenv ./mna.py [file]")
        exit(1)
    circuit_data = Parse(sys.argv[1])
