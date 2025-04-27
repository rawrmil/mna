# tbe
My Theoretical Basics of Electrotechnics fun little solvers

# MNA (Modified Nodal Analysis)
## Run using Pipenv
```bash
# INPUT: some-circuit-data.yaml
# EXAMPLES: mna/example
pip install pipenv
cd mna
pipenv run ./mna.py examples/linear1.yaml
# OUTPUT: in command line
# (in future) OUTPUT: solved.yaml
```

## Run using just Python
```bash
python3 mna/mna.py examples/linear1.yaml
```

## Writing custom circuits
```yaml
circuit:
  variables:
    # name: a-z/A-Z/0-9, type: real/complex
    - { name: a, type: real }
    - { name: b, type: complex }
  elements:
    # name: <string>, type: real/complex
    # type: voltage_source/current_source/resisor
    # nodes: [<integer/string>, <integer/string>]
    # parameters:
    #   voltage/current/resistance: <mathematica expression>
    - name: U0
      type: voltage_source
      nodes: [2, 1]
      parameters:
        voltage: "2*a-1"
    - name: R1
      type: resistor
      nodes: [1, 2]
      parameters:
        resistance: "b/3+1"
```

This YAML file represents circuit:
```text
.......Node 1........
...+-----+-----+.....
...|...........|.....
...|...........|.....
./ + \.......+[ ]....
.|   |.U0.....| |.R1.
.\ - /.......-[ ]....
...|...........|.....
...|...........|.....
...+-----+-----+.....
.......Node 2........
```
