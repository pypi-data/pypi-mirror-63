# hashable_ndframes

## Overview
`hashable_ndframes` provides subclasses `HashableSeries` and `HashableDataFrame` (of `pandas.Series` and `pandas.DataFrame`, respectively) which are hashable.

## Examples

```python
from pandas import Series
from hashable_ndframes import HashableSeries

# Series
s = HashableSeries(["a", "b", "c"])
assert isinstance(s, Series)

# equal Series, equal hash
hs = hash(s)
assert hash(HashableSeries(["a", "b", "c"])) == hs

# unequal Series, unequal hash
assert hash(HashableSeries(["a", "z", "c"])) != hs
assert hash(HashableSeries(["a", "b", "c"], name="other_name")) != hs
```
