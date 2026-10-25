# Choose rows and columns: loc (labels), iloc (positions), masks, query.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")   # Path(...).exists(): is that folder there?
df = pd.read_csv(DATA / "03_employees.csv")                          # pd.read_csv(): reads a CSV file into a table
emp = df.set_index("employee_id")     # .set_index("col"): makes that column the row labels

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Columns
print(df["name"].head(3))                 # df["col"]: one column; .head(3): first 3 rows
print(df[["name", "salary"]].head(3))     # df[[a, b]]: several columns

# %% iloc: by POSITION (end excluded)
print(df.iloc[0])                    # .iloc[n]: row by position number; first row
print(df.iloc[0:3])                  # rows 0, 1, 2
print(df.iloc[[0, 5, 10]])           # a list picks exactly those rows
print(df.iloc[0:3, 1:4])             # [rows, columns]: rows 0-2, columns 1-3
print(df.iloc[-1])                   # -1: the last row
print(df.iloc[:, 0:2].head(2))       # ":" means all rows; first 2 columns
print(df.iloc[2, 1])                 # one cell

# %% loc: by LABEL (end included)
print(emp.loc["E001"])                              # .loc[label]: row by its label
print(emp.loc["E001":"E003"])                       # label range, end included
print(emp.loc[["E001", "E010"], ["name", "salary"]])   # [row labels, column names]
print(emp.loc["E005", "name"])                      # one cell
print(df.loc[0:2, "name":"age"])                    # rows 0-2 and columns name to age
print(df.loc[df["salary"] > 100000, ["name", "salary"]])   # True/False test picks rows; list picks columns

# %% Boolean conditions
print(df[df["salary"] > 100000][["name", "salary"]])      # test gives True/False per row; keeps True rows
print(df[(df["department"] == "Engineering") & (df["remote"])][["name", "department"]])   # == equals; & = and (wrap tests in brackets)
print(df[(df["age"] < 25) | (df["age"] > 47)][["name", "age"]])   # | = or
print(df[~(df["department"] == "Sales")].shape)           # ~ = not (flips True/False); .shape: (rows, columns)
print(df[df["name"].str.startswith("A")]["name"].tolist())   # .str.startswith("A"): True if text begins with A

# %% isin, between, isna
print(df[df["department"].isin(["HR", "Finance"])].shape)    # .isin(list): True if value is in the list
print(df[~df["department"].isin(["HR", "Finance"])].shape)   # ~ : not in the list
print(df[df["salary"].between(60000, 70000)][["name", "salary"]])   # .between(a, b): True if from a to b
print(df[df["performance_score"].notna()].shape)             # .notna(): True where value is present

# %% query: SQL-like text
print(df.query("salary > 100000")[["name", "salary"]])      # .query("text"): filter rows using a text condition
print(df.query("department == 'Sales' and age > 35")[["name", "age"]])
limit = 90000
print(df.query("salary > @limit").shape)       # use a Python variable with @
print(df.query("department in ['HR', 'Finance']").shape)

# %% Top / bottom
print(df.nlargest(3, "salary")[["name", "salary"]])       # .nlargest(3, "col"): 3 rows with biggest values
print(df.nsmallest(3, "age")[["name", "age"]])            # .nsmallest(3, "col"): 3 rows with smallest values
print(df.sort_values("salary", ascending=False).head(3)[["name", "salary"]])   # .sort_values("col"): order rows; ascending=False: biggest first

# %% Change values safely (use loc, not chained brackets)
copy = df.copy()                                           # .copy(): independent duplicate
copy.loc[copy["salary"] < 55000, "salary"] = 55000         # .loc[rows test, col] = value: sets those cells
print(copy["salary"].min())                                # .min(): smallest value
copy.loc[copy["department"] == "HR", "department"] = "People"
print(copy["department"].unique())                         # .unique(): distinct values
copy.at[0, "name"] = "Aarav M."                            # .at[row, col] = value: sets one cell
print(copy.loc[0, "name"])

# %% Set / reset index
print(df.set_index("name").head(3))                        # column becomes the row labels
print(df.set_index(["department", "name"]).head(3))        # a list makes a two-level index
print(emp.reset_index().head(2))                           # .reset_index(): labels go back to a normal column
print(emp.sort_index(ascending=False).head(2))             # .sort_index(): order by row labels

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Filter columns by name pattern
print(df.filter(items=["name", "age"]).head(2))      # .filter(items=): keep columns with exactly these names
print(df.filter(like="e").columns.tolist())          # like="e": names containing "e"; .columns: names; .tolist(): plain list
print(df.filter(regex="^s").columns.tolist())        # regex=: a text pattern; "^s" = starts with s

# %% at / iat: fastest single cell
# .at[label, col]: one cell by labels; .iat[row, col]: one cell by positions.
print(emp.at["E001", "name"], df.iat[0, 1])

# %% where / mask (keep shape, hide the rest)
print(df["salary"].where(df["salary"] > 80000).head(5))   # .where(test): keeps items passing the test, others become NaN (empty)
print(df["salary"].mask(df["salary"] > 80000).head(5))    # .mask(test): the opposite, hides items passing the test

# %% First / unique rows
print(df.drop_duplicates(subset="department")[["department", "name"]])   # .drop_duplicates(subset=): keeps first row for each value
# .groupby("col"): groups rows by value; ["salary"].idxmax(): row label of biggest salary in each group.
print(df.loc[df.groupby("department")["salary"].idxmax(), ["department", "name", "salary"]])

# %% Reindex
print(df.head(3).reindex([2, 1, 0]))                       # .reindex(list): rows in this label order

# %% Sampling and slicing helpers
print(df.take([0, 2, 4])[["name"]])           # .take(list): rows at these positions
print(emp.xs("E001")["name"])                 # .xs(label): cross-section by index label
print(df[["name"]].squeeze().head(2))         # .squeeze(): one column -> Series
