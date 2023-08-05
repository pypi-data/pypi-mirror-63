
[![](https://codecov.io/gh/nickderobertis/transforms-fin/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/transforms-fin)

# transforms-fin

## Overview

A set of Transforms meant for financial analysis to be used with the datacode package

## Getting Started

Install `transforms_fin`:

```
pip install transforms_fin
```

A simple example:

```python
import transforms_fin  # transforms are automatically loaded upon import
import datacode as dc

a = dc.Variable('a', 'A')
vc = dc.VariableCollection(a)

# Portfolio transform
vc.a.port()

```

## Links

See the
[documentation here.](
https://nickderobertis.github.io/transforms-fin/
)

## Author

Created by Nick DeRobertis. MIT License.