# Create, change, and convert columns.
# Each line has a short comment saying WHAT the function is.

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

from pathlib import Path

import numpy as np
import pandas as pd

# Path(...).exists(): True if the folder exists. Path / "file" joins a folder and a file name.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file, parse_dates=[col]): loads a CSV file into a table; parse_dates turns that column into dates.
df = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])

# %% New columns from math
# df["new"] = ...: makes a new column. Series.round(n): rounds to n decimals (0 = whole numbers).
df["monthly"] = (df["salary"] / 12).round(0)
df["salary_k"] = df["salary"] / 1000
# df[["a", "b"]]: picks those columns. .head(n): first n rows.
print(df[["name", "salary", "monthly", "salary_k"]].head(3))

# %% assign: add columns in a chain (does not change the original)
# df.assign(col=function): returns a copy with new columns; lambda d: ... is a tiny function where d is the table.
out = df.assign(bonus=lambda d: d["salary"] * 0.1, total=lambda d: d["salary"] * 1.1)
print(out[["name", "bonus", "total"]].head(3))

# %% np.where: if / else
# np.where(test, a, b): picks a where the test is True, otherwise b.
df["senior"] = np.where(df["age"] >= 40, "Senior", "Junior")
# .value_counts(): counts how many times each value appears.
print(df["senior"].value_counts())

# %% np.select: many conditions
# np.select(conditions, labels, default=...): first matching condition picks the label; default is used if none match.
conditions = [df["salary"] < 60000, df["salary"] < 90000]
labels = ["Low", "Mid"]
df["band"] = np.select(conditions, labels, default="High")
print(df["band"].value_counts())

# %% cut and qcut: put numbers into buckets
# pd.cut(col, bins, labels): puts numbers into buckets; bins are the edges, labels name each bucket.
df["age_group"] = pd.cut(df["age"], bins=[0, 29, 39, 49, 100], labels=["20s", "30s", "40s", "50+"])
# .sort_index(): sorts by the row labels (here the bucket names).
print(df["age_group"].value_counts().sort_index())
# pd.qcut(col, q=4, labels): buckets with an equal number of rows in each (q=4: quarters).
df["salary_tier"] = pd.qcut(df["salary"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])  # equal sized groups
print(df["salary_tier"].value_counts().sort_index())
# bins=3: pandas makes 3 equal-width buckets for you.
print(pd.cut(df["age"], bins=3).head(3))

# %% map, apply, transform
# Series.map(dict or function): replaces each value using the dictionary/function; missing keys become NaN.
print(df["department"].map({"Engineering": "ENG", "Sales": "SAL"}).head(5))     # others -> NaN
# x[:3]: first 3 letters. .upper(): capital letters.
print(df["department"].map(lambda x: x[:3].upper()).head(3))
# Series.apply(function): runs the function on every value. .split(): breaks text into words.
print(df["name"].apply(lambda x: x.split()[0]).head(3))
# DataFrame.apply(function): runs it per column (np.mean = average).
print(df[["salary", "age"]].apply(np.mean))                       # per column
# axis=1: run the function once per row instead of per column.
print(df[["salary", "age"]].apply(lambda r: r["salary"] / r["age"], axis=1).head(3))   # per row
# DataFrame.map(function): runs the function on every single cell.
print(df[["salary", "age"]].map(lambda x: x * 2).head(2))         # every cell
# Series.transform(function): returns a result with the same length. .mean(): average. .std(): spread of values.
print(df["salary"].transform(lambda x: (x - x.mean()) / x.std()).round(2).head(3))

# %% Changing types
# .astype(type): converts the column to another type. .dtypes: shows the column type.
print(df["age"].astype(float).dtypes)
# "category": a type for columns with few repeated values.
print(df["employee_id"].astype("category").dtype)
# pd.to_numeric(x, errors="coerce"): turns text into numbers; bad text becomes NaN.
print(pd.to_numeric(pd.Series(["1", "2", "x"]), errors="coerce"))
# .tolist(): turns a column into a plain Python list. astype(int): True/False becomes 1/0.
print(df["remote"].astype(int).head(3).tolist())
# df.convert_dtypes(): switches columns to the best newer pandas types.
print(df.convert_dtypes().dtypes.head(4))

# %% Replace values
# Series.replace(dict): swaps old values for new ones.
print(df["gender"].replace({"M": "Male", "F": "Female"}).head(3))
# .unique(): list of distinct values. replace(old, new) also works with single values.
print(df["department"].replace("HR", "People").unique())
# replace(list, value): replaces every value in the list. range(20, 30): 20 to 29.
print(df["age"].replace(range(20, 30), 25).head(3))

# %% Sorting
# df.sort_values(col): sorts rows by that column (smallest first).
print(df.sort_values("salary").head(3)[["name", "salary"]])
# Several columns: sorts by the first, then the next. ascending=[True, False]: choose the direction for each.
print(df.sort_values(["department", "salary"], ascending=[True, False]).head(4)[["department", "salary"]])
# sort_index(): sorts by row labels. .index: the row labels.
print(df.sort_index(ascending=False).head(2).index.tolist())
# key=function: sorts using the changed version of the values. .str.lower(): small letters.
print(df.sort_values("name", key=lambda s: s.str.lower()).head(2)["name"].tolist())

# %% Duplicates
# df.duplicated(subset=[col]): True for rows whose col value was already seen. .sum(): adds up the Trues.
print(df.duplicated(subset=["department"]).sum())
# df.drop_duplicates(subset, keep): removes repeats; keep="first" keeps the first row, "last" the last. .shape: (rows, columns).
print(df.drop_duplicates(subset=["department"], keep="first").shape)
print(df.drop_duplicates(subset=["department"], keep="last")["name"].tolist())

# %% One-hot encoding (for machine learning)
# pd.get_dummies(col): makes one True/False column per category (one-hot).
print(pd.get_dummies(df["department"]).head(3))
# columns=[...]: only convert these columns. drop_first=True: skip the first category (it is implied). .columns: column names.
print(pd.get_dummies(df, columns=["gender"], drop_first=True).columns.tolist()[-3:])

# %% Drop and rename
# df.drop(columns=[...]): returns the table without those columns.
print(df.drop(columns=["monthly", "salary_k"]).shape)
# df.drop(index=[...]): returns the table without those rows (by label).
print(df.drop(index=[0, 1]).shape)
# df.rename(columns=...): changes column names; a function (str.upper = CAPITALS) is applied to every name.
print(df.rename(columns=str.upper).columns.tolist()[:3])
# A dictionary renames only the columns you list.
print(df.rename(columns={"salary": "pay"}).columns.tolist()[:6])
# df.add_prefix("x_") / add_suffix("_y"): adds text to the start / end of every column name.
print(df.add_prefix("x_").columns.tolist()[:2], df.add_suffix("_y").columns.tolist()[:2])

# %% Ranking and cumulative values
# Series.rank(): position of each value (1 = best). method="min": ties share the lowest rank.
df["salary_rank"] = df["salary"].rank(ascending=False, method="min")
# .cumsum(): running total down the column.
df["running_total"] = df["salary"].cumsum()
# Shows the new columns.
print(df[["name", "salary_rank", "running_total"]].head(3))
# .diff(): this row minus the previous row.
print(df["salary"].diff().head(3).tolist())
# .pct_change(): percent change from previous row (0.1 = 10%).
print(df["salary"].pct_change().round(3).head(3).tolist())
# .cummax() / .cummin(): biggest / smallest value so far.
print(df["salary"].cummax().head(3).tolist(), df["salary"].cummin().head(3).tolist())

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Clip and round
# .clip(lower, upper): values below lower become lower, above upper become upper.
print(df["salary"].clip(lower=60000, upper=100000).head(5))
# round(-3): negative rounds to thousands (12,345 -> 12,000).
print(df["performance_score"].round(0).head(3))
print(df["salary"].round(-3).head(3))

# %% Category type saves memory and enforces order
# pd.CategoricalDtype(list, ordered=True): a type with a fixed order of values (S < M < L).
sizes = pd.Series(["S", "L", "M", "S"], dtype=pd.CategoricalDtype(["S", "M", "L"], ordered=True))
# .cat.codes: the number of each category. .cat.categories: the list of categories.
print(sizes.sort_values().tolist(), sizes.cat.codes.tolist(), sizes.cat.categories.tolist())
# Comparison works because the categories have an order.
print(sizes > "S")

# %% Many-columns tricks
# df.eval("net = salary * 0.8"): makes a column from a text formula.
print(df.eval("net = salary * 0.8")[["salary", "net"]].head(2))
# df.agg([...]): runs several summary functions on each column.
print(df[["salary", "age"]].agg(["min", "max", "mean"]))
# df.pipe(function): passes the table into the function (handy in chains).
print(df[["salary", "age"]].pipe(lambda d: d / d.max()).head(2))
# .str.contains("sal"): True for names containing that text.
print(df.loc[:, df.columns.str.contains("sal")].columns.tolist())
# df.corr(): how strongly columns move together (-1 to 1). numeric_only=True: skip text columns. .loc[row, col]: pick one cell by label.
print(df.corr(numeric_only=True).round(2).loc["age", "salary"])
