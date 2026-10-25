# groupby = split into groups, calculate per group, combine.

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
df = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])

# %% The basics
print(df.groupby("department")["salary"].mean())
print(df.groupby("department")["salary"].sum())
print(df.groupby("department").size())               # rows per group
print(df.groupby("department")["salary"].count())
print(df.groupby("department")["salary"].agg(["min", "max", "mean", "median", "std"]))
print(df.groupby("department")["salary"].mean().sort_values(ascending=False))

# %% Several columns, several groups
print(df.groupby("department")[["salary", "age"]].mean())
print(df.groupby(["department", "gender"])["salary"].mean())
print(df.groupby(["department", "gender"])["salary"].mean().unstack())
print(df.groupby("department", as_index=False)["salary"].mean())

# %% agg with names (best way)
summary = df.groupby("department").agg(
    people=("employee_id", "count"),
    avg_salary=("salary", "mean"),
    top_salary=("salary", "max"),
    avg_age=("age", "mean"),
    remote_share=("remote", "mean"),
)
print(summary.round(2))

# %% agg with different functions per column
print(df.groupby("department").agg({"salary": ["mean", "max"], "age": "median"}))
print(df.groupby("department")["salary"].agg(lambda s: s.max() - s.min()))

# %% transform: result has the same length as the table
df["dept_avg"] = df.groupby("department")["salary"].transform("mean")
df["vs_dept"] = df["salary"] - df["dept_avg"]
df["pay_rank"] = df.groupby("department")["salary"].rank(ascending=False)
print(df[["name", "department", "salary", "dept_avg", "vs_dept", "pay_rank"]].head(5))

# %% filter: keep or drop whole groups
big = df.groupby("department").filter(lambda g: len(g) >= 6)
print(big["department"].unique())

# %% apply: any custom function per group
print(df.groupby("department")[["name", "salary"]].apply(lambda g: g.nlargest(1, "salary")))
print(df.groupby("department")["salary"].apply(lambda s: s.quantile(0.9)))

# %% Positions within a group
print(df.groupby("department").head(1)[["department", "name"]])       # first row of each
print(df.groupby("department").tail(1)[["department", "name"]])
print(df.groupby("department").nth(0)[["department", "name"]])
print(df.groupby("department").cumcount().head(5).tolist())
print(df.groupby("department").ngroup().head(5).tolist())

# %% Looking inside groups
grouped = df.groupby("department")
print(grouped.ngroups, list(grouped.groups.keys()))
print(grouped.get_group("HR")[["name", "salary"]])
for name, group in grouped:
    print(name, len(group))
    break

# %% Group by a calculated key
print(df.groupby(df["join_date"].dt.year)["employee_id"].count())
print(df.groupby(pd.cut(df["age"], [0, 30, 40, 100]), observed=True)["salary"].mean())
print(df.groupby(df["salary"] > 80000)["name"].count())

# %% Groups over time
print(df.groupby(pd.Grouper(key="join_date", freq="YE"))["employee_id"].count().head(4))

# %% Rolling and expanding inside groups
print(df.groupby("department")["salary"].cumsum().head(5).tolist())
print(df.groupby("department")["salary"].rolling(2).mean().head(3))
print(df.groupby("department")["salary"].shift(1).head(5).tolist())
print(df.groupby("department")["salary"].pct_change().head(5).round(3).tolist())

# %% pivot_table (Excel-style summary)
print(df.pivot_table(values="salary", index="department", columns="gender", aggfunc="mean"))
print(df.pivot_table(values="salary", index="department", aggfunc=["mean", "count"]))
print(df.pivot_table(values="salary", index="department", columns="gender", aggfunc="sum", margins=True))
print(df.pivot_table(values="salary", index="department", columns="remote", fill_value=0))

# %% crosstab: counts of combinations
print(pd.crosstab(df["department"], df["gender"]))
print(pd.crosstab(df["department"], df["gender"], normalize="index").round(2))
print(pd.crosstab(df["department"], df["remote"], margins=True))
print(pd.crosstab(df["department"], df["gender"], values=df["salary"], aggfunc="mean").round(0))

# %% Quick overall aggregations (no groups)
print(df["salary"].agg(["sum", "mean", "max"]))
print(df[["salary", "age"]].agg({"salary": "sum", "age": "mean"}))
print(df.describe().loc[["mean", "std"]])
