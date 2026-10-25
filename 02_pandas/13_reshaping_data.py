# Wide tables <-> long tables. Charts and models often want "long".

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])
print(monthly.head(3))        # WIDE: one column per category

# %% melt: wide -> long
long = monthly.melt(
    id_vars=["month", "visitors"],
    value_vars=["electronics", "clothing", "furniture"],
    var_name="category",
    value_name="sales",
)
print(long.head(6))
print(long.shape)

# %% pivot: long -> wide
wide = long.pivot(index="month", columns="category", values="sales")
print(wide.head(3))
print(wide.reset_index().head(3))

# %% pivot_table handles duplicates by aggregating
dup = pd.DataFrame({"k": ["a", "a", "b"], "c": ["x", "x", "y"], "v": [1, 3, 5]})
print(dup.pivot_table(index="k", columns="c", values="v", aggfunc="sum"))

# %% stack / unstack: move between index and columns
indexed = monthly.set_index("month")[["electronics", "clothing"]]
stacked = indexed.stack()
print(stacked.head(4))
print(stacked.unstack().head(2))
multi = long.groupby(["category", long["month"].dt.quarter])["sales"].sum()
print(multi)
print(multi.unstack(level=0))

# %% explode: a list in one cell -> many rows
tags = pd.DataFrame({"post": [1, 2], "tags": [["a", "b"], ["c"]]})
print(tags.explode("tags"))

# %% wide_to_long
scores = pd.DataFrame({"id": [1, 2], "math_2023": [80, 70], "math_2024": [85, 75]})
print(pd.wide_to_long(scores, stubnames="math", i="id", j="year", sep="_"))

# %% MultiIndex basics
mi = long.set_index(["category", "month"]).sort_index()
print(mi.loc["clothing"].head(2))
print(mi.loc[("clothing", "2023-03-01")])
print(mi.xs("2023-03-01", level="month"))
print(mi.index.names, mi.index.levels[0].tolist())
print(mi.reset_index().head(2))
print(mi.groupby(level="category")["sales"].sum())

# %% Transpose
print(monthly.set_index("month").head(2).T)

# %% Turn a column into dummies, split into pieces, and rank within groups
print(pd.get_dummies(long["category"]).head(3))
long["rank_in_cat"] = long.groupby("category")["sales"].rank(ascending=False)
print(long.sort_values(["category", "rank_in_cat"]).head(3))

# %% Chunk values into equal bins by position
print(pd.Series(range(10)).groupby(lambda i: i // 5).sum())
