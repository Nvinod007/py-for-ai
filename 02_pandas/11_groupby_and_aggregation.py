# groupby = split into groups, calculate per group, combine.
# Each line has a short comment saying WHAT the function is.

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

from pathlib import Path

import pandas as pd

# Path(...).exists(): True if the folder exists. Path / "file" joins a folder and a file name.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file, parse_dates=[col]): loads a CSV file into a table; parse_dates turns that column into dates.
df = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])

# %% The basics
# df.groupby(col): splits rows into groups by that column. ["salary"] picks a column; .mean() is the average per group.
print(df.groupby("department")["salary"].mean())
# .sum(): total per group.
print(df.groupby("department")["salary"].sum())
# .size(): number of rows in each group.
print(df.groupby("department").size())               # rows per group
# .count(): number of non-missing values per group.
print(df.groupby("department")["salary"].count())
# .agg([...]): runs several functions at once. median: middle value. std: how spread out values are.
print(df.groupby("department")["salary"].agg(["min", "max", "mean", "median", "std"]))
# .sort_values(ascending=False): biggest first.
print(df.groupby("department")["salary"].mean().sort_values(ascending=False))

# %% Several columns, several groups
# [["a", "b"]]: pick several columns.
print(df.groupby("department")[["salary", "age"]].mean())
# groupby([a, b]): groups by a combination of two columns.
print(df.groupby(["department", "gender"])["salary"].mean())
# .unstack(): turns the inner group level into columns.
print(df.groupby(["department", "gender"])["salary"].mean().unstack())
# as_index=False: keep the group as a normal column, not as the row label.
print(df.groupby("department", as_index=False)["salary"].mean())

# %% agg with names (best way)
# agg(name=(column, function)): makes named result columns. count counts rows; max is the biggest; mean of True/False = share of True.
summary = df.groupby("department").agg(
    people=("employee_id", "count"),
    avg_salary=("salary", "mean"),
    top_salary=("salary", "max"),
    avg_age=("age", "mean"),
    remote_share=("remote", "mean"),
)
# .round(2): rounds to 2 decimals.
print(summary.round(2))

# %% agg with different functions per column
# agg({col: function(s)}): a different function for each column.
print(df.groupby("department").agg({"salary": ["mean", "max"], "age": "median"}))
# lambda s: ...: a tiny function; s is the group's values. Here: biggest minus smallest.
print(df.groupby("department")["salary"].agg(lambda s: s.max() - s.min()))

# %% transform: result has the same length as the table
# .transform("mean"): group average, repeated on every row (same length as table).
df["dept_avg"] = df.groupby("department")["salary"].transform("mean")
df["vs_dept"] = df["salary"] - df["dept_avg"]
# .rank(ascending=False): rank inside each group (1 = highest).
df["pay_rank"] = df.groupby("department")["salary"].rank(ascending=False)
# .head(5): first 5 rows.
print(df[["name", "department", "salary", "dept_avg", "vs_dept", "pay_rank"]].head(5))

# %% pivot_table (Excel-style summary)
# df.pivot_table(values, index, columns, aggfunc): Excel-style summary; index = rows, columns = columns, aggfunc = how to combine.
print(df.pivot_table(values="salary", index="department", columns="gender", aggfunc="mean"))
# aggfunc=[...]: several functions at once.
print(df.pivot_table(values="salary", index="department", aggfunc=["mean", "count"]))
# margins=True: adds an "All" row and column with totals.
print(df.pivot_table(values="salary", index="department", columns="gender", aggfunc="sum", margins=True))
# fill_value=0: puts 0 where there is no data.
print(df.pivot_table(values="salary", index="department", columns="remote", fill_value=0))

# %% crosstab: counts of combinations
# pd.crosstab(a, b): table counting how often each combination happens.
print(pd.crosstab(df["department"], df["gender"]))
# normalize="index": show each row as a share of its row total (0 to 1).
print(pd.crosstab(df["department"], df["gender"], normalize="index").round(2))
# margins=True adds totals.
print(pd.crosstab(df["department"], df["remote"], margins=True))
# values + aggfunc: calculate something (here mean salary) instead of counting.
print(pd.crosstab(df["department"], df["gender"], values=df["salary"], aggfunc="mean").round(0))

# %% Quick overall aggregations (no groups)
# Series.agg([...]): several summaries of one column (no groups).
print(df["salary"].agg(["sum", "mean", "max"]))
# agg({col: function}): one function per column.
print(df[["salary", "age"]].agg({"salary": "sum", "age": "mean"}))
# df.describe(): count, mean, std, min, quartiles, max for number columns. .loc[[rows]]: pick rows by label.
print(df.describe().loc[["mean", "std"]])

# %% Group by a calculated key
# .dt.year: the year of each date. Grouping by a calculated column works too.
print(df.groupby(df["join_date"].dt.year)["employee_id"].count())
# pd.cut(col, edges): puts numbers into buckets. observed=True: only show buckets that have data.
print(df.groupby(pd.cut(df["age"], [0, 30, 40, 100]), observed=True)["salary"].mean())
# Grouping by a True/False test splits rows into two groups.
print(df.groupby(df["salary"] > 80000)["name"].count())

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% filter: keep or drop whole groups
# .filter(function): keeps only groups where the function returns True. len(g): rows in the group.
big = df.groupby("department").filter(lambda g: len(g) >= 6)
# .unique(): list of distinct values.
print(big["department"].unique())

# %% apply: any custom function per group
# .apply(function): runs your function on each group. .nlargest(n, col): rows with the n biggest values.
print(df.groupby("department")[["name", "salary"]].apply(lambda g: g.nlargest(1, "salary")))
# .quantile(0.9): value that 90% of the data is below.
print(df.groupby("department")["salary"].apply(lambda s: s.quantile(0.9)))

# %% Positions within a group
# groupby.head(1): first row of each group. .tail(1): last row.
print(df.groupby("department").head(1)[["department", "name"]])       # first row of each
print(df.groupby("department").tail(1)[["department", "name"]])
# .nth(0): the row at position 0 of each group.
print(df.groupby("department").nth(0)[["department", "name"]])
# .cumcount(): 0,1,2... position of each row inside its group. .tolist(): plain Python list.
print(df.groupby("department").cumcount().head(5).tolist())
# .ngroup(): the group number of each row.
print(df.groupby("department").ngroup().head(5).tolist())

# %% Looking inside groups
# Saving the groupby in a variable so we can look inside it.
grouped = df.groupby("department")
# .ngroups: number of groups. .groups: dictionary of groups; .keys(): their names.
print(grouped.ngroups, list(grouped.groups.keys()))
# .get_group(name): the rows of one group.
print(grouped.get_group("HR")[["name", "salary"]])
# Looping over a groupby gives (group name, group table). break stops after the first.
for name, group in grouped:
    print(name, len(group))
    break

# %% Groups over time
# pd.Grouper(key=date column, freq="YE"): groups dates by time chunk (YE = year end).
print(df.groupby(pd.Grouper(key="join_date", freq="YE"))["employee_id"].count().head(4))

# %% Rolling and expanding inside groups
# .cumsum(): running total inside each group.
print(df.groupby("department")["salary"].cumsum().head(5).tolist())
# .rolling(2).mean(): average of the last 2 rows inside each group.
print(df.groupby("department")["salary"].rolling(2).mean().head(3))
# .shift(1): previous row's value inside each group.
print(df.groupby("department")["salary"].shift(1).head(5).tolist())
# .pct_change(): percent change from the previous row.
print(df.groupby("department")["salary"].pct_change().head(5).round(3).tolist())
