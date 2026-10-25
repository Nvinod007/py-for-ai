# Combine tables: concat (stack), merge (SQL join), join (by index).

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
sales = pd.read_csv(DATA / "01_sales_messy.csv").drop_duplicates()
customers = pd.read_csv(DATA / "02_customers.csv")
print(sales.shape, customers.shape)

# %% concat: stack tables
a = pd.DataFrame({"id": [1, 2], "v": ["a", "b"]})
b = pd.DataFrame({"id": [3, 4], "v": ["c", "d"]})
print(pd.concat([a, b]))                                    # rows under rows
print(pd.concat([a, b], ignore_index=True))                 # fresh index
print(pd.concat([a, b], keys=["first", "second"]))          # label each piece
print(pd.concat([a, b.rename(columns={"v": "w"})], axis=1)) # side by side
extra = pd.DataFrame({"id": [9], "z": [1.5]})
print(pd.concat([a, extra]))                                # different columns -> NaN
print(pd.concat([a, extra], join="inner"))                  # only shared columns

# %% merge: the 4 join types
left = pd.DataFrame({"key": ["A", "B", "C"], "x": [1, 2, 3]})
right = pd.DataFrame({"key": ["B", "C", "D"], "y": [20, 30, 40]})
print(pd.merge(left, right, on="key", how="inner"))   # only keys in both
print(pd.merge(left, right, on="key", how="left"))    # all of left
print(pd.merge(left, right, on="key", how="right"))   # all of right
print(pd.merge(left, right, on="key", how="outer"))   # everything
print(pd.merge(left, right, how="cross").shape)             # every pair (no key)

# %% Keys with different names
emp = pd.DataFrame({"emp_id": [1, 2], "name": ["Asha", "Ben"]})
pay = pd.DataFrame({"person": [1, 2], "salary": [10, 20]})
print(pd.merge(emp, pay, left_on="emp_id", right_on="person").drop(columns="person"))

# %% Overlapping column names
l2 = pd.DataFrame({"k": [1, 2], "val": [10, 20]})
r2 = pd.DataFrame({"k": [1, 2], "val": [100, 200]})
print(pd.merge(l2, r2, on="k", suffixes=("_left", "_right")))

# %% Real example: sales + customers
merged = sales.merge(customers, on="customer_id", how="left", suffixes=("", "_cust"))
print(merged[["order_id", "customer_id", "customer_name", "name", "tier"]].head())
print(merged["tier"].isna().sum(), "orders have no customer record")

# %% Find unmatched rows with indicator
check = sales.merge(customers, on="customer_id", how="outer", indicator=True)
print(check["_merge"].value_counts())
print(check[check["_merge"] == "right_only"][["customer_id", "name"]])      # customers with no orders
print(check[check["_merge"] == "left_only"]["customer_id"].unique()[:5])    # orders with no customer

# %% validate: catch bad joins early
try:
    pd.merge(l2, pd.concat([r2, r2]), on="k", validate="one_to_one")
except pd.errors.MergeError as error:
    print("Error:", error)

# %% join: merge using the index
x = pd.DataFrame({"a": [1, 2]}, index=["r1", "r2"])
y = pd.DataFrame({"b": [3, 4]}, index=["r1", "r3"])
print(x.join(y))
print(x.join(y, how="outer"))
print(x.join(y, how="inner"))

# %% Multi-column keys
s1 = pd.DataFrame({"y": [2023, 2023], "m": [1, 2], "a": [5, 6]})
s2 = pd.DataFrame({"y": [2023, 2023], "m": [1, 2], "b": [7, 8]})
print(pd.merge(s1, s2, on=["y", "m"]))

# %% Fill gaps from another table
primary = pd.DataFrame({"v": [1.0, None, 3.0]})
backup = pd.DataFrame({"v": [10.0, 20.0, 30.0]})
print(primary.combine_first(backup))
print(primary.fillna(backup))

# %% Update values in place from another table
base = pd.DataFrame({"id": [1, 2], "score": [10, 20]}).set_index("id")
fix = pd.DataFrame({"id": [2], "score": [99]}).set_index("id")
base.update(fix)
print(base)

# %% Closest-time merge
trades = pd.DataFrame({"time": pd.to_datetime(["2024-01-01 10:00:03", "2024-01-01 10:00:09"]), "qty": [1, 2]})
quotes = pd.DataFrame({"time": pd.to_datetime(["2024-01-01 10:00:00", "2024-01-01 10:00:05"]), "price": [100, 101]})
print(pd.merge_asof(trades, quotes, on="time"))

# %% Compare two tables
t1 = pd.DataFrame({"a": [1, 2, 3]})
t2 = pd.DataFrame({"a": [1, 9, 3]})
print(t1.compare(t2))
print(t1.equals(t2))
