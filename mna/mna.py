#!/usr/bin/python3

# TODO: Strict typing

import sys
import yaml

def Parse(fname):
    # TODO: Structural checks
    circuit_file = open(sys.argv[1], "r")
    circuit = yaml.safe_load(circuit_file)
    circuit_file.close()

def Solve(circuit):
    pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        # TODO: Erro handling
        print("pipenv ./mna.py [file]")
        exit(1)
    Perse(sys.argv[1])
