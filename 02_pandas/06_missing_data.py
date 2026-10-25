# Missing data is the #1 problem in real datasets.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")   # Path(...).exists(): is that folder there?
sales = pd.read_csv(DATA / "01_sales_messy.csv")                     # pd.read_csv(): reads a CSV file into a table

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Find it
print(sales.isna().sum())                         # .isna(): True where missing; .sum(): counts the Trues per column
print(sales.isna().mean().round(3) * 100)         # .mean(): share of Trues; .round(3): 3 decimals; percent missing
print(sales[sales["rating"].isna()][["order_id", "rating"]])   # keeps rows where rating is missing
print(sales.isna().any(axis=1).sum())             # .any(axis=1): True if any gap across the row; rows with any gap
print(sales.notna().sum())                        # .notna(): True where value is present

# %% Small demo table
# np.nan: the "not a number / missing" marker; None: Python's "nothing".
df = pd.DataFrame(
    {
        "a": [1, np.nan, 3, np.nan, 5],
        "b": [np.nan, 20, 30, 40, np.nan],
        "c": ["x", "y", None, "y", "x"],
    }
)
print(df)

# %% Drop
print(df.dropna())                          # .dropna(): removes rows with missing values; any column missing -> row removed
print(df.dropna(how="all"))                 # how="all": only rows where everything is missing
print(df.dropna(subset=["a"]))              # subset=: only look at column a

# %% Fill with a value
print(df.fillna(0))                         # .fillna(0): replaces missing with 0
# fillna({col: value}): a different fill for each column; .mean(): average; .median(): middle value.
print(df.fillna({"a": df["a"].mean(), "b": df["b"].median(), "c": "unknown"}))
print(df["a"].fillna(df["a"].mean()))       # fills one column with its average

# %% Fill from neighbours
print(df.ffill())                           # .ffill(): copy last known value down
print(df.bfill())                           # .bfill(): copy next known value up
print(df.ffill(limit=1))                    # limit=1: fill at most 1 gap in a row

# %% Fill by group (smart fill)
emp = pd.DataFrame(
    {
        "dept": ["A", "A", "B", "B"],
        "pay": [100.0, np.nan, 200.0, np.nan],
    }
)
# .groupby("dept"): splits rows by department; .transform("mean"): each group's average, lined up with every row.
emp["pay"] = emp["pay"].fillna(emp.groupby("dept")["pay"].transform("mean"))
print(emp)

# %% Turn odd markers into NaN
odd = pd.DataFrame({"x": [1, -999, 3], "y": ["a", "N/A", "c"]})
print(odd.replace({-999: np.nan, "N/A": np.nan}))    # .replace({old: new}): swaps values
print(odd.replace(-999, np.nan))                     # replace one value
print(odd.replace(["N/A", -999], np.nan))            # a list replaces all of them with the same new value

# %% Aggregations skip NaN by default
# .sum() total, .mean() average, .count() number of non-missing values.
print(df["a"].sum(), df["a"].mean(), df["a"].count())
print(df["a"].sum(skipna=False))            # skipna=False: do not ignore missing, so result is NaN

# %% Clean the sales data
clean = sales.copy()
clean["rating"] = clean["rating"].fillna(clean["rating"].median())   # fill gaps with the middle value
clean["discount"] = clean["discount"].fillna(0)                      # fill gaps with 0
clean["city"] = clean["city"].fillna("Unknown")                      # fill gaps with text
print(clean.isna().sum())

# %% Flag missing instead of hiding it
sales["rating_missing"] = sales["rating"].isna()    # new True/False column
print(sales["rating_missing"].sum())                # .sum() on True/False: counts the Trues

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Drop (less common)
print(df.dropna(thresh=2))                  # thresh=2: keep rows with at least 2 real values
print(df.dropna(axis=1))                    # axis=1: work on columns; drop columns with gaps

# %% Fill by estimating
print(df[["a", "b"]].interpolate())         # df[[a, b]]: pick columns; .interpolate(): guesses gaps from values around them
# method="linear": straight-line guess; limit_direction="both": also fill gaps at the start and end.
print(df[["a", "b"]].interpolate(method="linear", limit_direction="both"))

# %% Compare with NaN (NaN == NaN is False)
print(np.nan == np.nan)                     # == asks "equal?"; NaN is never equal to anything
print(df["a"].eq(df["a"]).tolist())         # .eq(): the == check on every item; .tolist(): plain list
print(df.equals(df.copy()))                 # .equals(): same data (treats NaN as equal); .copy(): independent duplicate
