# Missing data is the #1 problem in real datasets.

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
sales = pd.read_csv(DATA / "01_sales_messy.csv")

# %% Find it
print(sales.isna().sum())
print(sales.isna().mean().round(3) * 100)         # percent missing
print(sales[sales["rating"].isna()][["order_id", "rating"]])
print(sales.isna().any(axis=1).sum())             # rows with any gap
print(sales.notna().sum())

# %% Small demo table
df = pd.DataFrame(
    {
        "a": [1, np.nan, 3, np.nan, 5],
        "b": [np.nan, 20, 30, 40, np.nan],
        "c": ["x", "y", None, "y", "x"],
    }
)
print(df)

# %% Drop
print(df.dropna())                          # any column missing -> row removed
print(df.dropna(how="all"))                 # only rows where everything is missing
print(df.dropna(subset=["a"]))              # only look at column a
print(df.dropna(thresh=2))                  # keep rows with at least 2 real values
print(df.dropna(axis=1))                    # drop columns with gaps

# %% Fill with a value
print(df.fillna(0))
print(df.fillna({"a": df["a"].mean(), "b": df["b"].median(), "c": "unknown"}))
print(df["a"].fillna(df["a"].mean()))

# %% Fill from neighbours
print(df.ffill())                           # copy last known value down
print(df.bfill())                           # copy next known value up
print(df.ffill(limit=1))

# %% Fill by estimating
print(df[["a", "b"]].interpolate())
print(df[["a", "b"]].interpolate(method="linear", limit_direction="both"))

# %% Fill by group (smart fill)
emp = pd.DataFrame(
    {
        "dept": ["A", "A", "B", "B"],
        "pay": [100.0, np.nan, 200.0, np.nan],
    }
)
emp["pay"] = emp["pay"].fillna(emp.groupby("dept")["pay"].transform("mean"))
print(emp)

# %% Turn odd markers into NaN
odd = pd.DataFrame({"x": [1, -999, 3], "y": ["a", "N/A", "c"]})
print(odd.replace({-999: np.nan, "N/A": np.nan}))
print(odd.replace(-999, np.nan))
print(odd.replace(["N/A", -999], np.nan))

# %% Aggregations skip NaN by default
print(df["a"].sum(), df["a"].mean(), df["a"].count())
print(df["a"].sum(skipna=False))

# %% Compare with NaN (NaN == NaN is False)
print(np.nan == np.nan)
print(df["a"].eq(df["a"]).tolist())
print(df.equals(df.copy()))

# %% Clean the sales data
clean = sales.copy()
clean["rating"] = clean["rating"].fillna(clean["rating"].median())
clean["discount"] = clean["discount"].fillna(0)
clean["city"] = clean["city"].fillna("Unknown")
print(clean.isna().sum())

# %% Flag missing instead of hiding it
sales["rating_missing"] = sales["rating"].isna()
print(sales["rating_missing"].sum())
