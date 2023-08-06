# OpenTEA description
[![build
status](https://nitrox.cerfacs.fr/opentea/opentea/badges/develop/build.svg)](https://nitrox.cerfacs.fr/opentea/opentea/commits/develop)
[![coverage
report](https://nitrox.cerfacs.fr/opentea/opentea/badges/develop/coverage.svg)](https://nitrox.cerfacs.fr/opentea/opentea/commits/develop)

Welcome to the OpenTEA GUI Engine and nested objects handling! 

The documentation is currently in [nitrox pages](http://opentea.pg.cerfacs.fr/opentea), soon moving to readTheDocs.



## Installation 

Opentea is OpenSource (Cecill-B) available on PiPY. 

```
pip install opentea
```

## Basic Usage

OpenTEA is, at first a Graphival User Interface engine, based on the json-SCHEMA description.

Assume a nested information conforming to the following SCHEMA :

```yaml
---
title: "Trivial form..."
type: object
properties:
  first_tab:
    type: object
    title: Only tab.
    process: custom_callback.py
    properties:
      first_block:
        type: object
        title: Custom Block
        properties:
          number_1:
            title: "Number 1"
            type: number
            default: 32.
          operand:
            title: "Operation"
            type: string
            default: "+"
            enum: ["+", "-", "*", "/"]
          number_2:
            title: "Number 2"
            type: number
            default: 10.
          result:
            title: "result"
            state: disabled
            type: string
            default: "-"
```

The openTEA GUI wil show as :
![Trivial GUI](/src/gallery/trivial.png)

In this form, a callback can be added to each tab.
The corresponding `custom_callback.py` script is :

```python
"""Module for the first tab."""

from opentea.noob.noob import nob_get, nob_set
from opentea.process_utils import process_tab


def custom_fun(nob_in):
    """Update result."""
    nob_out = nob_in.copy()
    operation = nob_get(nob_in, "operand")
    nb1 = nob_get(nob_in, "number_1")
    nb2 = nob_get(nob_in, "number_2")
    if operation == "+":
        res = nb1 + nb2
    elif operation == "-":
        res = nb1 - nb2
    elif operation == "*":
        res = nb1 * nb2
    elif operation == "/":
        res = nb1 / nb2
    else:
        res = None
    nob_set(nob_out, res, "result")
    return nob_out

if __name__ == "__main__":
    process_tab(custom_fun)
```

Finally, the data recoded by the GUI is available as a YAML file, conforming to the SCHEMA Validation:

```yaml
first_tab:
  first_block:
    number_1: 32.0
    number_2: 10.0
    operand: +
    result: 42.0
```


