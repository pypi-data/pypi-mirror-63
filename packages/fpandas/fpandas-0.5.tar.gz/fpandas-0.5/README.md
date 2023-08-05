# Functional Pandas

_**tools for a [monad](https://en.wikipedia.org/wiki/Monad_(functional_programming))
-inspired [pandas](https://pandas.pydata.org/) design pattern**._

The next logical step after [The Unreasonable Effectiveness of Method-Chaining](https://towardsdatascience.com/the-unreasonable-effectiveness-of-method-chaining-in-pandas-15c2109e3c69)
by Adiamaan Keerthi, which you must read if you haven't.

## Example
```python
import pandas as pd
import fpandas as fpd

df = ...

@fpd.SafePiper('print')
def drop_stuff(dataframe: pd.DataFrame) -> pd.DataFrame:
  return dataframe.drop(['x2, x3'], axis=1)

@fpd.SafePiper('print')
def fail(dataframe: pd.DataFrame) -> pd.DataFrame:
  return jskdbeosquabfjfdsal  # NameError

@fpd.SafePiper('print')
def impute(dataframe: pd.DataFrame) -> pd.DataFrame:
  return dataframe.fillna('foo')

fpd.pipe(
  (impute, fail, drop_stuff),
  df
) # gently prints the name of the function that failed and returns None

fpd.pipe(
  (impute, drop_stuff),
  df
) # returns a DataFrame
```

