# A DataFrame is a table: rows + columns. Each column is a Series.

import numpy as np
import pandas as pd

# %% From a dict of columns (most common)
df = pd.DataFrame(
    {
        "name": ["Asha", "Ben", "Chen", "Divya"],
        "age": [25, 32, 47, 29],
        "city": ["Pune", "Delhi", "Pune", "Mumbai"],
        "salary": [50000, 64000, 90000, 58000],
    }
)
print(df)

# %% From a list of rows (dicts)
rows = [
    {"name": "Asha", "age": 25},
    {"name": "Ben", "age": 32, "city": "Delhi"},  # missing keys become NaN
]
print(pd.DataFrame(rows))

# %% From lists + column names
print(pd.DataFrame([[1, "a"], [2, "b"]], columns=["num", "letter"]))

# %% From NumPy
print(pd.DataFrame(np.arange(6).reshape(2, 3), columns=["a", "b", "c"]))
print(pd.DataFrame(np.random.default_rng(0).random((3, 2)), columns=["x", "y"]))

# %% With a custom index
print(pd.DataFrame({"v": [1, 2, 3]}, index=["r1", "r2", "r3"]))

# %% Basic facts
print(df.shape)          # (rows, columns)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.size, df.ndim, len(df))
print(df.values)         # NumPy array
print(df.axes)
print(df.empty)

# %% Getting one or more columns
print(df["name"])                 # Series
print(df[["name", "salary"]])     # DataFrame
print(df.name)                    # shortcut, avoid (fails on odd names)

# %% Adding columns
df["bonus"] = df["salary"] * 0.1
df["country"] = "India"
df["senior"] = df["age"] > 30
print(df)

# %% Deleting
df = df.drop(columns=["country"])
print(df.columns.tolist())
popped = df.pop("senior")         # removes AND returns it
print(popped.tolist())

# %% Renaming
print(df.rename(columns={"name": "full_name"}))
df.columns = [c.upper() for c in df.columns]
print(df.columns.tolist())
df.columns = df.columns.str.lower()

# %% Reorder columns
print(df[["city", "name", "age", "salary", "bonus"]])
df.insert(1, "id", [101, 102, 103, 104])   # insert at position 1
print(df)

# %% Transpose
print(df.T)

# %% Convert out
print(df.to_dict())
print(df.to_dict(orient="records"))
print(df.to_numpy())
print(df.to_string(index=False))

# %% Copy
backup = df.copy()
backup["age"] = 0
print(df["age"].tolist())   # unchanged, copy is independent
