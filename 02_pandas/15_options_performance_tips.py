# Display settings, speed, and memory tips.

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
df = pd.read_csv(DATA / "03_employees.csv")

# %% Display options
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 20)
pd.set_option("display.width", 120)
pd.set_option("display.float_format", "{:,.2f}".format)
print(df.describe())
print(pd.get_option("display.max_rows"))
pd.reset_option("display.float_format")

with pd.option_context("display.max_rows", 3):
    print(df)

# %% Styling output (Jupyter shows colors, here it is just an object)
styled = df.head(3).style.format({"salary": "{:,.0f}"}).highlight_max(subset=["salary"])
print(type(styled))

# %% Memory: smaller types
print(df.memory_usage(deep=True).sum())
small = df.copy()
small["age"] = small["age"].astype("int8")
small["department"] = small["department"].astype("category")
small["gender"] = small["gender"].astype("category")
small["salary"] = pd.to_numeric(small["salary"], downcast="integer")
print(small.memory_usage(deep=True).sum())
print(small.dtypes)

# %% Speed: avoid Python loops
big = pd.DataFrame({"a": np.arange(100_000), "b": np.arange(100_000)})
slow = [row.a + row.b for row in big.head(1000).itertuples()]   # works, but slow
fast = big["a"] + big["b"]                                      # vectorized
print(len(slow), fast.head(3).tolist())

# %% Looping when you really must
for row in df.head(2).itertuples(index=False):
    print(row.name, row.salary)
for index, row in df.head(1).iterrows():
    print(index, row["name"])
for column, series in df.iloc[:, :2].items():
    print(column, series.iloc[0])

# %% Method chaining: readable pipelines
result = (
    df.query("age > 30")
    .assign(monthly=lambda d: d["salary"] / 12)
    .groupby("department", as_index=False)["monthly"]
    .mean()
    .round(0)
    .sort_values("monthly", ascending=False)
)
print(result)

# %% Views vs copies: always use .copy() before changing a slice
subset = df[df["department"] == "HR"].copy()
subset["salary"] = 0
print(df[df["department"] == "HR"]["salary"].head(2).tolist())

# %% Useful extras
print(df.sample(frac=1, random_state=0).head(2)["name"].tolist())    # shuffle
print(df.nunique().sort_values().head(3))
print(df.columns.duplicated().any())
print(pd.__version__)
print(df.attrs)
print(df.pipe(len))
# df.head(3).to_clipboard()   # copies the table so you can paste into Excel
