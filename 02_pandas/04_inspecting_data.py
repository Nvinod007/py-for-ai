# First thing to do with any new dataset: look at it.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")   # Path: a folder/file path; .exists(): is it there?
df = pd.read_csv(DATA / "03_employees.csv")                          # pd.read_csv(): reads a CSV file into a table

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Look at rows
print(df.head())          # .head(): first 5 rows
print(df.head(3))         # .head(3): first 3 rows
print(df.tail(3))         # .tail(3): last 3 rows

# %% Structure
print(df.shape)                         # .shape: (rows, columns)
print(df.columns.tolist())              # .columns: column names; .tolist(): as a plain list
print(df.dtypes)                        # .dtypes: data type of each column
df.info()                               # .info(): types + non-null counts + memory

# %% Summary statistics
print(df.describe())                    # .describe(): count, mean, min, max... (numbers only)
print(df.describe(include="all"))       # include="all": every column, not just numbers

# %% Unique values and counts
print(df["department"].unique())        # .unique(): the distinct values
print(df["department"].nunique())       # .nunique(): how many distinct values
print(df["department"].value_counts())  # .value_counts(): how many times each value appears
print(df["department"].value_counts(normalize=True).round(2))   # normalize=True: shares; .round(2): 2 decimals
print(df.nunique())                     # unique count per column
print(df[["department", "gender"]].value_counts())   # df[[a, b]]: several columns; counts each combination

# %% Missing and duplicates
print(df.isna().sum())                  # .isna(): True where value is missing; .sum(): counts the Trues
print(df.isna().any().any())            # .any(): True if at least one True; twice = whole table
print(df.duplicated().sum())            # .duplicated(): True for repeated rows
print(df["name"].is_unique)             # .is_unique: True if no value repeats

# %% Single-number helpers
# .mean() average, .median() middle value, .std() spread of values.
print(df["salary"].mean(), df["salary"].median(), df["salary"].std())
# .min() smallest, .max() biggest, .sum() total.
print(df["salary"].min(), df["salary"].max(), df["salary"].sum())

# %% Column types
print(df.select_dtypes(include="number").columns.tolist())   # .select_dtypes(include=): keep columns of that type
print(df.select_dtypes(exclude="number").columns.tolist())   # exclude=: drop columns of that type
print(df.select_dtypes(include="bool").columns.tolist())     # bool: True/False columns

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Random sampling
print(df.sample(3, random_state=1))     # .sample(3): 3 random rows; random_state=1: same picks every run
print(df.sample(frac=0.1, random_state=1))   # frac=0.1: pick 10% of the rows

# %% Memory usage
print(df.memory_usage(deep=True))       # .memory_usage(): bytes used per column; deep=True: count text exactly

# %% Summary statistics (less common)
print(df["salary"].describe(percentiles=[0.1, 0.9]))   # df["col"]: one column; percentiles=: extra cut points
print(df.describe(include="number").T)  # include="number": numeric columns; .T: flips rows and columns

# %% Single-number helpers (less common)
print(df["salary"].quantile([0.25, 0.5, 0.75]))   # .quantile(): value below which that share of rows fall
print(df["age"].mode())                 # .mode(): most common value
print(df["salary"].skew(), df["salary"].kurt())   # .skew(): lean to one side; .kurt(): how heavy the tails are
print(df["salary"].count())             # non-missing count
print(df[["age", "salary"]].corr())     # .corr(): relationship between columns (-1 to 1)
print(df[["age", "salary"]].cov())      # .cov(): how two columns vary together
# .idxmax(): row label of the biggest value; df.loc[row, col]: pick a cell by labels.
print(df["salary"].idxmax(), df.loc[df["salary"].idxmax(), "name"])

# %% Quick checks
print(len(df))                          # len(): number of rows
print(df.columns.get_loc("salary"))     # .get_loc("name"): position number of that column
print("salary" in df.columns)            # `in`: is it in the list? True/False
print(df.index.is_unique)               # .index: row labels; .is_unique: none repeated?
print(df["salary"].between(60000, 90000).sum())   # .between(a, b): True if from a to b; .sum() counts them
print(df.equals(df.copy()))             # .equals(): same data?; .copy(): independent duplicate
