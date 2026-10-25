# A Series is ONE column: values + an index (labels).

import numpy as np
import pandas as pd

# %% Creating
s = pd.Series([10, 20, 30])
print(s)

named = pd.Series([85, 90, 78], index=["math", "science", "english"], name="marks")
print(named)

from_dict = pd.Series({"a": 1, "b": 2, "c": 3})
print(from_dict)
print(pd.Series(5, index=["x", "y", "z"]))     # same value repeated
print(pd.Series(np.arange(3.0)))

# %% Parts of a Series
print(named.values)       # the numbers (a NumPy array)
print(named.index)        # the labels
print(named.name, named.dtype, named.shape, named.size)

# %% Getting items
print(named["math"])
print(named.iloc[0])                  # by position
print(named[["math", "english"]])     # several labels
print(named["math":"science"])        # label slice includes the end
print(named.iloc[0:2])                # position slice excludes the end
print(named.loc["math"])

# %% Math on a Series
print(named + 5)
print(named * 2)
print(named / named.sum())
print(named > 80)
print(named[named > 80])

# %% Aggregations
print(named.sum(), named.mean(), named.median(), named.min(), named.max())
print(named.std(), named.var(), named.prod())
print(named.describe())
print(named.idxmax(), named.idxmin())       # label of biggest / smallest
print(named.nlargest(2), named.nsmallest(1))
print(named.cumsum())
print(named.quantile(0.5))

# %% Sorting
print(named.sort_values())
print(named.sort_values(ascending=False))
print(named.sort_index())
print(named.rank())

# %% Counting values
colors = pd.Series(["red", "blue", "red", "green", "red", "blue"])
print(colors.value_counts())
print(colors.value_counts(normalize=True))   # as a share
print(colors.unique(), colors.nunique())
print(colors.mode())
print(colors.duplicated().tolist())
print(colors.drop_duplicates())

# %% Changing values
print(named.map({"math": "M", "science": "S", "english": "E"}))
print(named.apply(lambda x: x + 10))
print(named.replace(90, 95))
print(named.where(named > 80, 0))
print(named.clip(lower=80))
print(named.round(-1))
print(named.astype(float))
print(named.rename("scores"))
print(named.rename(index={"math": "maths"}))

# %% Missing values
m = pd.Series([1, np.nan, 3, None])
print(m.isna().tolist(), m.notna().tolist())
print(m.dropna())
print(m.fillna(0))
print(m.ffill())
print(m.count(), m.size)

# %% Add / remove items
n = named.copy()
n["history"] = 70
print(n)
n = n.drop("math")
print(n)
print(pd.concat([named, pd.Series({"art": 88})]))

# %% Checks
print("math" in named)
print(named.isin([85, 78]))
print(named.between(80, 90))
print(named.is_unique, named.is_monotonic_increasing)

# %% Convert
print(named.to_list())
print(named.to_dict())
print(named.to_frame())
print(named.reset_index())
