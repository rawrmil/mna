# MNA (Modified Nodal Analysis)
## Run using Pipenv
```bash
pip install pipenv
# or [packege] install python3-pipenv
pipenv run python3 mna.py "1-2 VS_1 {u=10}; 2-1 R_2 {r="Sqrt[2]"}"
```

## Mini-WIKI
```text
Write each element in format:

<node1> <node2> <type>_<name> {<properties>}

separated by ';'

Element types:
- VS - voltage source (requires "u")
- CS - current source (requires "i")
- R - Resistor (requires "r")
```
