# Choose rows and columns: loc (labels), iloc (positions), masks, query.

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
df = pd.read_csv(DATA / "03_employees.csv")
emp = df.set_index("employee_id")

# %% Columns
print(df["name"].head(3))
print(df[["name", "salary"]].head(3))
print(df.filter(items=["name", "age"]).head(2))
print(df.filter(like="e").columns.tolist())          # names containing "e"
print(df.filter(regex="^s").columns.tolist())        # names starting with s

# %% iloc: by POSITION (end excluded)
print(df.iloc[0])                    # first row
print(df.iloc[0:3])
print(df.iloc[[0, 5, 10]])
print(df.iloc[0:3, 1:4])
print(df.iloc[-1])
print(df.iloc[:, 0:2].head(2))
print(df.iloc[2, 1])                 # one cell

# %% loc: by LABEL (end included)
print(emp.loc["E001"])
print(emp.loc["E001":"E003"])
print(emp.loc[["E001", "E010"], ["name", "salary"]])
print(emp.loc["E005", "name"])
print(df.loc[0:2, "name":"age"])
print(df.loc[df["salary"] > 100000, ["name", "salary"]])

# %% at / iat: fastest single cell
print(emp.at["E001", "name"], df.iat[0, 1])

# %% Boolean conditions
print(df[df["salary"] > 100000][["name", "salary"]])
print(df[(df["department"] == "Engineering") & (df["remote"])][["name", "department"]])
print(df[(df["age"] < 25) | (df["age"] > 47)][["name", "age"]])
print(df[~(df["department"] == "Sales")].shape)
print(df[df["name"].str.startswith("A")]["name"].tolist())

# %% isin, between, isna
print(df[df["department"].isin(["HR", "Finance"])].shape)
print(df[~df["department"].isin(["HR", "Finance"])].shape)
print(df[df["salary"].between(60000, 70000)][["name", "salary"]])
print(df[df["performance_score"].notna()].shape)

# %% query: SQL-like text
print(df.query("salary > 100000")[["name", "salary"]])
print(df.query("department == 'Sales' and age > 35")[["name", "age"]])
limit = 90000
print(df.query("salary > @limit").shape)       # use a Python variable with @
print(df.query("department in ['HR', 'Finance']").shape)

# %% where / mask (keep shape, hide the rest)
print(df["salary"].where(df["salary"] > 80000).head(5))
print(df["salary"].mask(df["salary"] > 80000).head(5))

# %% Top / bottom
print(df.nlargest(3, "salary")[["name", "salary"]])
print(df.nsmallest(3, "age")[["name", "age"]])
print(df.sort_values("salary", ascending=False).head(3)[["name", "salary"]])

# %% First / unique rows
print(df.drop_duplicates(subset="department")[["department", "name"]])
print(df.loc[df.groupby("department")["salary"].idxmax(), ["department", "name", "salary"]])

# %% Change values safely (use loc, not chained brackets)
copy = df.copy()
copy.loc[copy["salary"] < 55000, "salary"] = 55000
print(copy["salary"].min())
copy.loc[copy["department"] == "HR", "department"] = "People"
print(copy["department"].unique())
copy.at[0, "name"] = "Aarav M."
print(copy.loc[0, "name"])

# %% Set / reset index
print(df.set_index("name").head(3))
print(df.set_index(["department", "name"]).head(3))
print(emp.reset_index().head(2))
print(emp.sort_index(ascending=False).head(2))
print(df.head(3).reindex([2, 1, 0]))

# %% Sampling and slicing helpers
print(df.take([0, 2, 4])[["name"]])
print(emp.xs("E001")["name"])                 # cross-section by index label
print(df[["name"]].squeeze().head(2))         # one column -> Series
