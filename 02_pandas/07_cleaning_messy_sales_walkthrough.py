# A full cleaning job on data/01_sales_messy.csv, one problem at a time.
# Problems hidden in this file: extra spaces, mixed case, "$" in prices,
# mixed date formats, missing values, duplicates, negative and huge quantities.

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")

# %% Step 0: load and look
raw = pd.read_csv(DATA / "01_sales_messy.csv")
df = raw.copy()
print(df.shape)
print(df.head(10))
df.info()

# %% Step 1: clean column names (habit for every project)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns.tolist())

# %% Step 2: exact duplicate rows
print("duplicates:", df.duplicated().sum())
print(df[df.duplicated(keep=False)])
df = df.drop_duplicates()
print(df.shape)

# %% Step 3: whitespace and letter case in text columns
df["customer_name"] = df["customer_name"].str.strip().str.title()
df["city"] = df["city"].str.strip().str.title()
df["status"] = df["status"].str.strip().str.lower()
df["payment_method"] = df["payment_method"].str.strip().str.title()
print(df["customer_name"].head(3).tolist())
print(df["status"].value_counts())
print(df["payment_method"].value_counts())

# %% Step 4: prices are text like "$1,200.00"
print(df["unit_price"].dtype)
df["unit_price"] = (
    df["unit_price"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)
print(df["unit_price"].describe())

# %% Step 5: dates in different formats
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")
print(df["order_date"].dtype)
print(df["order_date"].min(), df["order_date"].max())

# %% Step 6: missing values (look first, then decide per column)
print(df.isna().sum())
df["city"] = df["city"].fillna("Unknown")
df["discount"] = df["discount"].fillna(0.0)
df["rating"] = df["rating"].fillna(df["rating"].median())
# unit_price missing: fill with typical price of the same product
df["unit_price"] = df["unit_price"].fillna(
    df.groupby("product")["unit_price"].transform("median")
)
print(df.isna().sum())

# %% Step 7: impossible or extreme values
print(df[df["quantity"] <= 0])                # a return, negative quantity
print(df["quantity"].describe())
q1, q3 = df["quantity"].quantile([0.25, 0.75])
iqr = q3 - q1
upper = q3 + 1.5 * iqr
print("outlier limit:", upper)
print(df[df["quantity"] > upper][["order_id", "product", "quantity"]])

df["is_return"] = df["quantity"] < 0
df["quantity"] = df["quantity"].clip(upper=upper)     # cap extreme values
df = df[df["quantity"] != 0]

# %% Step 8: right data types
df["order_id"] = df["order_id"].astype(int)
df["quantity"] = df["quantity"].round().astype(int)
df["rating"] = df["rating"].astype(int)
for column in ["category", "payment_method", "status", "city"]:
    df[column] = df[column].astype("category")
df.info()

# %% Step 9: new useful columns
df["gross"] = df["quantity"] * df["unit_price"]
df["net_revenue"] = df["gross"] * (1 - df["discount"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)
df["weekday"] = df["order_date"].dt.day_name()
print(df[["order_id", "gross", "net_revenue", "month", "weekday"]].head())

# %% Step 10: sanity checks (stop if something is still wrong)
assert df["order_id"].is_unique, "order ids should be unique"
assert df["unit_price"].notna().all()
assert df["discount"].between(0, 1).all()
print("checks passed")

# %% Step 11: save the clean file
out = DATA / "output"
out.mkdir(exist_ok=True)
df.sort_values("order_id").to_csv(out / "sales_clean.csv", index=False)
print(pd.read_csv(out / "sales_clean.csv").head())

# %% Compare before and after
print(raw.shape, "->", df.shape)
print(raw.dtypes)
print(df.dtypes)
