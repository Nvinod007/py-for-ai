# A Series is ONE column: values + an index (labels).
# Each line has a short comment saying WHAT the function is.

import numpy as np
import pandas as pd

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Creating
# pd.Series(list): makes one column of values with labels 0, 1, 2...
s = pd.Series([10, 20, 30])
# print(x): shows x on screen.
print(s)

# index=: your own labels; name=: a title for the column.
named = pd.Series([85, 90, 78], index=["math", "science", "english"], name="marks")
print(named)

# pd.Series(dict): dict keys become the labels, dict values become the values.
from_dict = pd.Series({"a": 1, "b": 2, "c": 3})
print(from_dict)
print(pd.Series(5, index=["x", "y", "z"]))     # same value repeated
# np.arange(3.0): numbers 0.0, 1.0, 2.0 (NumPy's version of range).
print(pd.Series(np.arange(3.0)))

# %% Parts of a Series
print(named.values)       # .values: the numbers (a NumPy array)
print(named.index)        # .index: the labels
# .name: column title; .dtype: type of data; .shape: (count,); .size: how many items.
print(named.name, named.dtype, named.shape, named.size)

# %% Getting items
print(named["math"])                  # s["label"]: get one item by its label
print(named.iloc[0])                  # .iloc[n]: get by position number (starts at 0)
print(named[["math", "english"]])     # a list of labels gives several items
print(named["math":"science"])        # label slice includes the end
print(named.iloc[0:2])                # position slice excludes the end
print(named.loc["math"])              # .loc[label]: get by label (explicit form)

# %% Math on a Series
# + - * / work on every item at once.
print(named + 5)
print(named * 2)
print(named / named.sum())            # .sum(): adds all items
print(named > 80)                     # > gives True/False for each item
print(named[named > 80])              # True/False list as index keeps only True items

# %% Aggregations
# .sum() total, .mean() average, .median() middle value, .min()/.max() smallest/biggest.
print(named.sum(), named.mean(), named.median(), named.min(), named.max())

# %% Sorting
print(named.sort_values())                      # .sort_values(): order by value, smallest first
print(named.sort_values(ascending=False))       # ascending=False: biggest first
print(named.sort_index())                       # .sort_index(): order by label (A to Z)
print(named.rank())                             # .rank(): 1 = smallest, 2 = next, ...

# %% Counting values
colors = pd.Series(["red", "blue", "red", "green", "red", "blue"])
print(colors.value_counts())                 # .value_counts(): how many times each value appears
print(colors.value_counts(normalize=True))   # as a share
# .unique(): distinct values; .nunique(): how many distinct values.
print(colors.unique(), colors.nunique())

# %% Changing values
print(named.map({"math": "M", "science": "S", "english": "E"}))   # .map(dict): swaps each value using the dict
print(named.apply(lambda x: x + 10))         # .apply(f): runs function f on every item; lambda = tiny one-line function
print(named.replace(90, 95))                 # .replace(old, new): swaps one value for another

# %% Missing values
# np.nan / None: "no value here" markers.
m = pd.Series([1, np.nan, 3, None])
# .isna(): True where missing; .notna(): True where present.
print(m.isna().tolist(), m.notna().tolist())
print(m.dropna())                            # .dropna(): removes missing items
print(m.fillna(0))                           # .fillna(0): replaces missing with 0
print(m.ffill())                             # .ffill(): fills missing with the value above
print(m.count(), m.size)                     # .count(): non-missing items; .size: all items

# %% Convert
print(named.to_list())                       # .to_list(): plain Python list
print(named.to_dict())                       # .to_dict(): dict of label -> value
print(named.to_frame())                      # .to_frame(): turn into a 1-column table
print(named.reset_index())                   # .reset_index(): labels become a normal column

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Aggregations (less common)
# .std() spread of values, .var() spread squared, .prod() multiplies all items.
print(named.std(), named.var(), named.prod())
print(named.describe())                     # .describe(): quick summary (count, mean, min, max...)
print(named.idxmax(), named.idxmin())       # label of biggest / smallest
# .nlargest(n): top n values; .nsmallest(n): bottom n values.
print(named.nlargest(2), named.nsmallest(1))
print(named.cumsum())                       # .cumsum(): running total
print(named.quantile(0.5))                  # .quantile(0.5): value below which 50% of items fall

# %% Counting values (less common)
print(colors.mode())                         # .mode(): most common value
print(colors.duplicated().tolist())          # .duplicated(): True if seen before; .tolist(): to a plain list
print(colors.drop_duplicates())              # .drop_duplicates(): keeps first of each value

# %% Changing values (less common)
print(named.where(named > 80, 0))            # .where(test, 0): keeps items passing the test, others become 0
print(named.clip(lower=80))                  # .clip(lower=80): anything below 80 becomes 80
print(named.round(-1))                       # .round(-1): round to nearest 10
print(named.astype(float))                   # .astype(float): change data type to decimals
print(named.rename("scores"))                # .rename("x"): change the Series name
print(named.rename(index={"math": "maths"})) # .rename(index={old: new}): change a label

# %% Add / remove items
n = named.copy()                             # .copy(): independent duplicate
n["history"] = 70                            # s["new label"] = value: adds an item
print(n)
n = n.drop("math")                           # .drop("label"): removes that item
print(n)
# pd.concat([a, b]): joins Series/tables one after another.
print(pd.concat([named, pd.Series({"art": 88})]))

# %% Checks
print("math" in named)                       # `in` checks the labels
print(named.isin([85, 78]))                  # .isin(list): True if value is in the list
print(named.between(80, 90))                 # .between(a, b): True if value is from a to b
# .is_unique: no repeated values?; .is_monotonic_increasing: always going up?
print(named.is_unique, named.is_monotonic_increasing)
