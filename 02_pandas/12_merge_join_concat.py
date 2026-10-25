# Combine tables: concat (stack), merge (SQL join), join (by index).
# Each line has a short comment saying WHAT the function is.

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

from pathlib import Path

import pandas as pd

# Path(...).exists(): True if the folder exists. Path / "file" joins a folder and a file name.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV file into a table. .drop_duplicates(): removes repeated rows.
sales = pd.read_csv(DATA / "01_sales_messy.csv").drop_duplicates()
customers = pd.read_csv(DATA / "02_customers.csv")
# .shape: (number of rows, number of columns).
print(sales.shape, customers.shape)

# %% concat: stack tables
# pd.DataFrame({col: [values]}): builds a small table from a dictionary.
a = pd.DataFrame({"id": [1, 2], "v": ["a", "b"]})
b = pd.DataFrame({"id": [3, 4], "v": ["c", "d"]})
# pd.concat([t1, t2]): glues tables together (default: one under the other).
print(pd.concat([a, b]))                                    # rows under rows
# ignore_index=True: renumber the rows 0,1,2...
print(pd.concat([a, b], ignore_index=True))                 # fresh index
# keys=[...]: adds an outer label for each piece.
print(pd.concat([a, b], keys=["first", "second"]))          # label each piece
# axis=1: place tables side by side. .rename(columns={old: new}): changes a column name.
print(pd.concat([a, b.rename(columns={"v": "w"})], axis=1)) # side by side
# Tables with different columns get NaN (missing) where data is absent.
extra = pd.DataFrame({"id": [9], "z": [1.5]})
print(pd.concat([a, extra]))                                # different columns -> NaN
# join="inner": keep only columns both tables have.
print(pd.concat([a, extra], join="inner"))                  # only shared columns

# %% merge: the 4 join types
# A table that has the key column "key".
left = pd.DataFrame({"key": ["A", "B", "C"], "x": [1, 2, 3]})
right = pd.DataFrame({"key": ["B", "C", "D"], "y": [20, 30, 40]})
# pd.merge(left, right, on=col, how=...): joins tables by matching values in col. inner = only matches.
print(pd.merge(left, right, on="key", how="inner"))   # only keys in both
# left: keep all rows of the left table.
print(pd.merge(left, right, on="key", how="left"))    # all of left
# right: keep all rows of the right table.
print(pd.merge(left, right, on="key", how="right"))   # all of right
# outer: keep all rows of both.
print(pd.merge(left, right, on="key", how="outer"))   # everything
# cross: every row paired with every row (no key needed).
print(pd.merge(left, right, how="cross").shape)             # every pair (no key)

# %% Keys with different names
# left_on / right_on: the key column has a different name in each table.
emp = pd.DataFrame({"emp_id": [1, 2], "name": ["Asha", "Ben"]})
pay = pd.DataFrame({"person": [1, 2], "salary": [10, 20]})
# Then .drop(columns="person") removes the extra key column.
print(pd.merge(emp, pay, left_on="emp_id", right_on="person").drop(columns="person"))

# %% Overlapping column names
# Both tables have a column called val.
l2 = pd.DataFrame({"k": [1, 2], "val": [10, 20]})
r2 = pd.DataFrame({"k": [1, 2], "val": [100, 200]})
# suffixes=(a, b): text added to same-named columns so you can tell them apart.
print(pd.merge(l2, r2, on="k", suffixes=("_left", "_right")))

# %% Real example: sales + customers
# left_table.merge(right, ...): same as pd.merge. Empty suffix "" leaves the left name unchanged.
merged = sales.merge(customers, on="customer_id", how="left", suffixes=("", "_cust"))
# .head(): first 5 rows.
print(merged[["order_id", "customer_id", "customer_name", "name", "tier"]].head())
# .isna(): True where missing. .sum(): counts the Trues.
print(merged["tier"].isna().sum(), "orders have no customer record")

# %% Find unmatched rows with indicator
# indicator=True: adds a _merge column saying where each row came from (both / left_only / right_only).
check = sales.merge(customers, on="customer_id", how="outer", indicator=True)
# .value_counts(): counts each distinct value.
print(check["_merge"].value_counts())
# check[test]: keeps rows where the test is True.
print(check[check["_merge"] == "right_only"][["customer_id", "name"]])      # customers with no orders
# .unique(): distinct values. [:5]: first five of them.
print(check[check["_merge"] == "left_only"]["customer_id"].unique()[:5])    # orders with no customer

# %% join: merge using the index
# index=[...]: the row labels.
x = pd.DataFrame({"a": [1, 2]}, index=["r1", "r2"])
y = pd.DataFrame({"b": [3, 4]}, index=["r1", "r3"])
# x.join(y): joins using the row labels (index). Default keeps rows of x.
print(x.join(y))
# how="outer": keep rows from both tables. "inner": only rows in both.
print(x.join(y, how="outer"))
print(x.join(y, how="inner"))

# %% Multi-column keys
# on=[a, b]: match on two columns together.
s1 = pd.DataFrame({"y": [2023, 2023], "m": [1, 2], "a": [5, 6]})
s2 = pd.DataFrame({"y": [2023, 2023], "m": [1, 2], "b": [7, 8]})
print(pd.merge(s1, s2, on=["y", "m"]))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% validate: catch bad joins early
# try / except: run code and handle an error instead of crashing.
try:
    # validate="one_to_one": raises an error if the join is not one row to one row.
    pd.merge(l2, pd.concat([r2, r2]), on="k", validate="one_to_one")
# pd.errors.MergeError: the error type raised for bad merges.
except pd.errors.MergeError as error:
    print("Error:", error)

# %% Fill gaps from another table
# None in a list becomes NaN (missing).
primary = pd.DataFrame({"v": [1.0, None, 3.0]})
backup = pd.DataFrame({"v": [10.0, 20.0, 30.0]})
# df.combine_first(other): fills missing cells from the other table.
print(primary.combine_first(backup))
# df.fillna(x): fills missing cells with x (here the matching cells of another table).
print(primary.fillna(backup))

# %% Update values in place from another table
# .set_index(col): uses that column as the row labels.
base = pd.DataFrame({"id": [1, 2], "score": [10, 20]}).set_index("id")
fix = pd.DataFrame({"id": [2], "score": [99]}).set_index("id")
# df.update(other): overwrites values with those from the other table (changes df itself).
base.update(fix)
print(base)

# %% Closest-time merge
# pd.to_datetime(list): converts text to real dates/times.
trades = pd.DataFrame({"time": pd.to_datetime(["2024-01-01 10:00:03", "2024-01-01 10:00:09"]), "qty": [1, 2]})
quotes = pd.DataFrame({"time": pd.to_datetime(["2024-01-01 10:00:00", "2024-01-01 10:00:05"]), "price": [100, 101]})
# pd.merge_asof(a, b, on=time): matches each row with the closest earlier time in b.
print(pd.merge_asof(trades, quotes, on="time"))

# %% Compare two tables
t1 = pd.DataFrame({"a": [1, 2, 3]})
t2 = pd.DataFrame({"a": [1, 9, 3]})
# df.compare(other): shows only the cells that differ.
print(t1.compare(t2))
# df.equals(other): True if both tables are exactly the same.
print(t1.equals(t2))
