# A DataFrame is a table: rows + columns. Each column is a Series.
# Each line has a short comment saying WHAT the function is.

import numpy as np
import pandas as pd

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% From a dict of columns (most common)
# pd.DataFrame(dict): makes a table; each key is a column name, each list is its values.
df = pd.DataFrame(
    {
        "name": ["Asha", "Ben", "Chen", "Divya"],
        "age": [25, 32, 47, 29],
        "city": ["Pune", "Delhi", "Pune", "Mumbai"],
        "salary": [50000, 64000, 90000, 58000],
    }
)
print(df)                # print(x): shows x on screen

# %% From a list of rows (dicts)
rows = [
    {"name": "Asha", "age": 25},
    {"name": "Ben", "age": 32, "city": "Delhi"},  # missing keys become NaN (NaN = "no value")
]
print(pd.DataFrame(rows))                         # a list of dicts: each dict is one row

# %% From lists + column names
# columns=: names for the columns.
print(pd.DataFrame([[1, "a"], [2, "b"]], columns=["num", "letter"]))

# %% With a custom index
# index=: your own row labels instead of 0, 1, 2.
print(pd.DataFrame({"v": [1, 2, 3]}, index=["r1", "r2", "r3"]))

# %% Basic facts
print(df.shape)          # .shape: (rows, columns)
print(df.columns)        # .columns: the column names
print(df.index)          # .index: the row labels
print(df.dtypes)         # .dtypes: data type of each column

# %% Getting one or more columns
print(df["name"])                 # df["col"]: one column (a Series)
print(df[["name", "salary"]])     # df[["a", "b"]]: several columns (a DataFrame)
print(df.name)                    # shortcut, avoid (fails on odd names)

# %% Adding columns
df["bonus"] = df["salary"] * 0.1  # df["new"] = ...: creates a column; * works on every row
df["country"] = "India"           # one value repeated for every row
df["senior"] = df["age"] > 30     # > gives True/False for each row
print(df)

# %% Deleting
df = df.drop(columns=["country"])         # df.drop(columns=[...]): removes those columns
print(df.columns.tolist())                # .tolist(): turns into a plain Python list
popped = df.pop("senior")         # df.pop("col"): removes AND returns it
print(popped.tolist())

# %% Renaming
print(df.rename(columns={"name": "full_name"}))   # df.rename(columns={old: new}): renames columns
df.columns = [c.upper() for c in df.columns]      # sets all names; .upper(): CAPITAL letters
print(df.columns.tolist())
df.columns = df.columns.str.lower()               # .str.lower(): makes text small letters

# %% Copy
backup = df.copy()                         # .copy(): independent duplicate
backup["age"] = 0
print(df["age"].tolist())   # unchanged, copy is independent

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Basic facts (less common)
# .size: total cells; .ndim: number of dimensions (2 for a table); len(df): number of rows.
print(df.size, df.ndim, len(df))
print(df.values)         # .values: the data as a NumPy array
print(df.axes)           # .axes: the row labels and column names together
print(df.empty)          # .empty: True if the table has no data

# %% From NumPy
# np.arange(6): numbers 0..5; .reshape(2, 3): arrange them into 2 rows x 3 columns.
print(pd.DataFrame(np.arange(6).reshape(2, 3), columns=["a", "b", "c"]))
# np.random.default_rng(0): random number maker (0 = fixed start so results repeat); .random((3, 2)): 3x2 numbers between 0 and 1.
print(pd.DataFrame(np.random.default_rng(0).random((3, 2)), columns=["x", "y"]))

# %% Reorder columns
print(df[["city", "name", "age", "salary", "bonus"]])   # list columns in the order you want
df.insert(1, "id", [101, 102, 103, 104])   # df.insert(pos, name, values): adds a column at position 1
print(df)

# %% Transpose
print(df.T)              # .T: flips rows and columns

# %% Convert out
print(df.to_dict())                        # .to_dict(): dict of columns
print(df.to_dict(orient="records"))        # orient="records": list of one dict per row
print(df.to_numpy())                       # .to_numpy(): NumPy array of the data
print(df.to_string(index=False))           # .to_string(): table as text; index=False hides row labels
