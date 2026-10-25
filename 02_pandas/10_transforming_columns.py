# Create, change, and convert columns.

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
df = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])

# %% New columns from math
df["monthly"] = (df["salary"] / 12).round(0)
df["salary_k"] = df["salary"] / 1000
print(df[["name", "salary", "monthly", "salary_k"]].head(3))

# %% assign: add columns in a chain (does not change the original)
out = df.assign(bonus=lambda d: d["salary"] * 0.1, total=lambda d: d["salary"] * 1.1)
print(out[["name", "bonus", "total"]].head(3))

# %% np.where: if / else
df["senior"] = np.where(df["age"] >= 40, "Senior", "Junior")
print(df["senior"].value_counts())

# %% np.select: many conditions
conditions = [df["salary"] < 60000, df["salary"] < 90000]
labels = ["Low", "Mid"]
df["band"] = np.select(conditions, labels, default="High")
print(df["band"].value_counts())

# %% cut and qcut: put numbers into buckets
df["age_group"] = pd.cut(df["age"], bins=[0, 29, 39, 49, 100], labels=["20s", "30s", "40s", "50+"])
print(df["age_group"].value_counts().sort_index())
df["salary_tier"] = pd.qcut(df["salary"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])  # equal sized groups
print(df["salary_tier"].value_counts().sort_index())
print(pd.cut(df["age"], bins=3).head(3))

# %% map, apply, transform
print(df["department"].map({"Engineering": "ENG", "Sales": "SAL"}).head(5))     # others -> NaN
print(df["department"].map(lambda x: x[:3].upper()).head(3))
print(df["name"].apply(lambda x: x.split()[0]).head(3))
print(df[["salary", "age"]].apply(np.mean))                       # per column
print(df[["salary", "age"]].apply(lambda r: r["salary"] / r["age"], axis=1).head(3))   # per row
print(df[["salary", "age"]].map(lambda x: x * 2).head(2))         # every cell
print(df["salary"].transform(lambda x: (x - x.mean()) / x.std()).round(2).head(3))

# %% Changing types
print(df["age"].astype(float).dtypes)
print(df["employee_id"].astype("category").dtype)
print(pd.to_numeric(pd.Series(["1", "2", "x"]), errors="coerce"))
print(df["remote"].astype(int).head(3).tolist())
print(df.convert_dtypes().dtypes.head(4))

# %% Replace values
print(df["gender"].replace({"M": "Male", "F": "Female"}).head(3))
print(df["department"].replace("HR", "People").unique())
print(df["age"].replace(range(20, 30), 25).head(3))

# %% Clip and round
print(df["salary"].clip(lower=60000, upper=100000).head(5))
print(df["performance_score"].round(0).head(3))
print(df["salary"].round(-3).head(3))

# %% Sorting
print(df.sort_values("salary").head(3)[["name", "salary"]])
print(df.sort_values(["department", "salary"], ascending=[True, False]).head(4)[["department", "salary"]])
print(df.sort_index(ascending=False).head(2).index.tolist())
print(df.sort_values("name", key=lambda s: s.str.lower()).head(2)["name"].tolist())

# %% Ranking and cumulative values
df["salary_rank"] = df["salary"].rank(ascending=False, method="min")
df["running_total"] = df["salary"].cumsum()
print(df[["name", "salary_rank", "running_total"]].head(3))
print(df["salary"].diff().head(3).tolist())
print(df["salary"].pct_change().round(3).head(3).tolist())
print(df["salary"].cummax().head(3).tolist(), df["salary"].cummin().head(3).tolist())

# %% Duplicates
print(df.duplicated(subset=["department"]).sum())
print(df.drop_duplicates(subset=["department"], keep="first").shape)
print(df.drop_duplicates(subset=["department"], keep="last")["name"].tolist())

# %% One-hot encoding (for machine learning)
print(pd.get_dummies(df["department"]).head(3))
print(pd.get_dummies(df, columns=["gender"], drop_first=True).columns.tolist()[-3:])

# %% Category type saves memory and enforces order
sizes = pd.Series(["S", "L", "M", "S"], dtype=pd.CategoricalDtype(["S", "M", "L"], ordered=True))
print(sizes.sort_values().tolist(), sizes.cat.codes.tolist(), sizes.cat.categories.tolist())
print(sizes > "S")

# %% Drop and rename
print(df.drop(columns=["monthly", "salary_k"]).shape)
print(df.drop(index=[0, 1]).shape)
print(df.rename(columns=str.upper).columns.tolist()[:3])
print(df.rename(columns={"salary": "pay"}).columns.tolist()[:6])
print(df.add_prefix("x_").columns.tolist()[:2], df.add_suffix("_y").columns.tolist()[:2])

# %% Many-columns tricks
print(df.eval("net = salary * 0.8")[["salary", "net"]].head(2))
print(df[["salary", "age"]].agg(["min", "max", "mean"]))
print(df[["salary", "age"]].pipe(lambda d: d / d.max()).head(2))
print(df.loc[:, df.columns.str.contains("sal")].columns.tolist())
print(df.corr(numeric_only=True).round(2).loc["age", "salary"])
