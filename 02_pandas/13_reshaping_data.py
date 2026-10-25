# Wide tables <-> long tables. Charts and models often want "long".
# Each line has a short comment saying WHAT the function is.

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

from pathlib import Path

import pandas as pd

# Path(...).exists(): True if the folder exists. Path / "file" joins a folder and a file name.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file, parse_dates=[col]): loads a CSV file; parse_dates turns that column into dates.
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])
# .head(n): first n rows.
print(monthly.head(3))        # WIDE: one column per category

# %% melt: wide -> long
# df.melt(): wide -> long. id_vars stay as they are; value_vars are stacked into rows.
long = monthly.melt(
    id_vars=["month", "visitors"],
    value_vars=["electronics", "clothing", "furniture"],
    # var_name / value_name: names of the two new columns (old column names / their values).
    var_name="category",
    value_name="sales",
)
print(long.head(6))
# .shape: (rows, columns).
print(long.shape)

# %% pivot: long -> wide
# df.pivot(index, columns, values): long -> wide; each value in columns becomes a new column.
wide = long.pivot(index="month", columns="category", values="sales")
print(wide.head(3))
# .reset_index(): moves the row labels back into a normal column.
print(wide.reset_index().head(3))

# %% pivot_table handles duplicates by aggregating
# pd.DataFrame({...}): builds a table from a dictionary.
dup = pd.DataFrame({"k": ["a", "a", "b"], "c": ["x", "x", "y"], "v": [1, 3, 5]})
# df.pivot_table(index, columns, values, aggfunc): like pivot but combines duplicates (aggfunc="sum" adds them).
print(dup.pivot_table(index="k", columns="c", values="v", aggfunc="sum"))

# %% explode: a list in one cell -> many rows
# A cell can hold a whole list.
tags = pd.DataFrame({"post": [1, 2], "tags": [["a", "b"], ["c"]]})
# df.explode(col): one row for each item in the list.
print(tags.explode("tags"))

# %% Transpose
# .T: transpose (swap rows and columns).
print(monthly.set_index("month").head(2).T)

# %% Turn a column into dummies, split into pieces, and rank within groups
# pd.get_dummies(col): one True/False column per category.
print(pd.get_dummies(long["category"]).head(3))
# .rank(ascending=False): 1 = biggest value inside the group.
long["rank_in_cat"] = long.groupby("category")["sales"].rank(ascending=False)
# df.sort_values([a, b]): sort by a, then b.
print(long.sort_values(["category", "rank_in_cat"]).head(3))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% stack / unstack: move between index and columns
# df.set_index(col): uses that column as the row labels.
indexed = monthly.set_index("month")[["electronics", "clothing"]]
# df.stack(): turns columns into an extra row level (wide -> long Series).
stacked = indexed.stack()
print(stacked.head(4))
# .unstack(): the opposite of stack; moves a row level back to columns.
print(stacked.unstack().head(2))
# .groupby([...])[col].sum(): total per group. .dt.quarter: quarter (1-4) of each date.
multi = long.groupby(["category", long["month"].dt.quarter])["sales"].sum()
print(multi)
# level=0: move the first index level (category) to columns.
print(multi.unstack(level=0))

# %% wide_to_long
# Columns like math_2023, math_2024 hide a year inside the name.
scores = pd.DataFrame({"id": [1, 2], "math_2023": [80, 70], "math_2024": [85, 75]})
# pd.wide_to_long(df, stubnames, i, j, sep): splits those names into a base (math) and a year column.
print(pd.wide_to_long(scores, stubnames="math", i="id", j="year", sep="_"))

# %% MultiIndex basics
# .set_index([a, b]): two-level row labels (MultiIndex). .sort_index(): sorts by labels.
mi = long.set_index(["category", "month"]).sort_index()
# .loc[label]: picks rows by label (here the first level).
print(mi.loc["clothing"].head(2))
# .loc[(a, b)]: picks by both levels.
print(mi.loc[("clothing", "2023-03-01")])
# .xs(value, level=name): picks rows by one level's value.
print(mi.xs("2023-03-01", level="month"))
# .index.names: level names. .index.levels[0]: distinct values of level 0.
print(mi.index.names, mi.index.levels[0].tolist())
# .reset_index() makes the levels normal columns again.
print(mi.reset_index().head(2))
# groupby(level=name): group by an index level.
print(mi.groupby(level="category")["sales"].sum())

# %% Chunk values into equal bins by position
# pd.Series(range(10)): column holding 0..9. groupby(function): the function gets each index and returns its group (i // 5 = whole-number division).
print(pd.Series(range(10)).groupby(lambda i: i // 5).sum())
