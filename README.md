# tbe
My Theoretical Basics of Electrotechnics fun little solvers

# MNA (Modified Nodal Analysis)
## Running
```bash
# INPUT: somecirc.yams
# EXAMPLES: mna/example
pip install pipenv
cd mna
pipenv run ./mna.py examples/linear1.yaml
# OUTPUT: in command line
# (in future) OUTPUT: solved.yaml
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
    - name: u0
      type: voltage_source
      nodes: [2, 1]
      parameters:
        voltage: "a-1"
    - name: r2
      type: resistor
      nodes: [1, 2]
      parameters:
        resistance: "b+1"
```
