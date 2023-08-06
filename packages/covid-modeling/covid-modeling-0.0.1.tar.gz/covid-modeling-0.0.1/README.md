# COMODELS

Models for COVID - 19

For documentation, see the docstrings!
Much more to come

## Penn model

```python
# import the penn model
from comodels.sir import Penn

print(Penn.__doc__)
tx = Penn(28304596, 223, 0)

print(Penn.sir.__doc__)
curve, occupancy = tx.sir(n_days = 23)

print(curve.keys())
print(occupancy())
```
