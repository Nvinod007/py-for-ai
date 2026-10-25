# Display settings, speed, and memory tips.
# Each line has a short comment saying WHAT the function is.

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

from pathlib import Path

import numpy as np
import pandas as pd

# Path(...).exists(): True if the folder exists. Path / "file" joins a folder and a file name.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV file into a table.
df = pd.read_csv(DATA / "03_employees.csv")

# %% Display options
# pd.set_option(name, value): changes how pandas prints. max_columns: columns shown.
pd.set_option("display.max_columns", 50)
# max_rows: rows shown before pandas cuts the middle.
pd.set_option("display.max_rows", 20)
# width: characters per line.
pd.set_option("display.width", 120)
# float_format: how decimals print; "{:,.2f}".format = commas and 2 decimals.
pd.set_option("display.float_format", "{:,.2f}".format)
# df.describe(): count, mean, min, max... of number columns.
print(df.describe())
# pd.get_option(name): reads the current setting.
print(pd.get_option("display.max_rows"))
# pd.reset_option(name): sets it back to default.
pd.reset_option("display.float_format")

# %% Speed: avoid Python loops
# np.arange(n): numbers 0 to n-1. pd.DataFrame({...}): builds a table.
big = pd.DataFrame({"a": np.arange(100_000), "b": np.arange(100_000)})
# .itertuples(): loops over rows as named tuples (row.a). .head(1000): first 1000 rows.
slow = [row.a + row.b for row in big.head(1000).itertuples()]   # works, but slow
# Column + column adds all rows at once (vectorized).
fast = big["a"] + big["b"]                                      # vectorized
# len(x): number of items. .tolist(): plain Python list.
print(len(slow), fast.head(3).tolist())

# %% Looping when you really must
# index=False: leave out the row label.
for row in df.head(2).itertuples(index=False):
    print(row.name, row.salary)
# .iterrows(): loops giving (row label, row as Series).
for index, row in df.head(1).iterrows():
    print(index, row["name"])
# .iloc[rows, cols]: pick by position; [:, :2] = all rows, first 2 columns. .items(): loops giving (column name, column).
for column, series in df.iloc[:, :2].items():
    print(column, series.iloc[0])

# %% Method chaining: readable pipelines
# df.query("text"): filters rows using a text condition. Each .method() passes its result to the next (a chain).
result = (
    df.query("age > 30")
    # .assign(col=function): adds a column.
    .assign(monthly=lambda d: d["salary"] / 12)
    # .groupby(col)[col2].mean(): average per group; as_index=False keeps group as a column.
    .groupby("department", as_index=False)["monthly"]
    .mean()
    .round(0)
    # .sort_values(col, ascending=False): biggest first.
    .sort_values("monthly", ascending=False)
)
print(result)

# %% Views vs copies: always use .copy() before changing a slice
# .copy() makes a safe separate table so changing it does not touch df.
subset = df[df["department"] == "HR"].copy()
subset["salary"] = 0
# df[test]: keep rows where the test is True.
print(df[df["department"] == "HR"]["salary"].head(2).tolist())

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Display option_context
# pd.option_context(name, value): changes a setting only inside the with block.
with pd.option_context("display.max_rows", 3):
    print(df)

# %% Styling output (Jupyter shows colors, here it is just an object)
# df.style: table with colours. .format({col: pattern}): number display. .highlight_max(subset=[col]): colours the biggest.
styled = df.head(3).style.format({"salary": "{:,.0f}"}).highlight_max(subset=["salary"])
# type(x): tells what kind of object x is.
print(type(styled))

# %% Memory: smaller types
# df.memory_usage(deep=True): bytes used by each column. .sum(): total.
print(df.memory_usage(deep=True).sum())
# df.copy(): an independent copy.
small = df.copy()
# .astype(type): converts the column. int8: small whole numbers (-128 to 127).
small["age"] = small["age"].astype("int8")
# "category": efficient type for repeated text.
small["department"] = small["department"].astype("category")
small["gender"] = small["gender"].astype("category")
# pd.to_numeric(col, downcast="integer"): picks the smallest integer type that fits.
small["salary"] = pd.to_numeric(small["salary"], downcast="integer")
print(small.memory_usage(deep=True).sum())
# .dtypes: type of each column.
print(small.dtypes)

# %% Useful extras
# df.sample(frac=1, random_state=0): random rows; frac=1 = all rows shuffled; random_state fixes the shuffle.
print(df.sample(frac=1, random_state=0).head(2)["name"].tolist())    # shuffle
# df.nunique(): number of distinct values per column. .sort_values(): smallest first.
print(df.nunique().sort_values().head(3))
# .columns.duplicated(): True for repeated column names. .any(): True if any is True.
print(df.columns.duplicated().any())
# pd.__version__: the pandas version number.
print(pd.__version__)
# df.attrs: a dictionary for notes attached to the table.
print(df.attrs)
# df.pipe(function): passes df into the function (len = row count).
print(df.pipe(len))
# df.head(3).to_clipboard()   # copies the table so you can paste into Excel
