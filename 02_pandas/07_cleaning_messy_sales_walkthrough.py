# A full cleaning job on data/01_sales_messy.csv, one problem at a time.
# Each line has a short comment saying WHAT the function is.
# Problems hidden in this file: extra spaces, mixed case, "$" in prices,
# mixed date formats, missing values, duplicates, negative and huge quantities.

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")   # Path(...).exists(): is that folder there?

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Step 0: load and look
raw = pd.read_csv(DATA / "01_sales_messy.csv")     # pd.read_csv(): reads a CSV file into a table
df = raw.copy()                                    # .copy(): independent duplicate, raw stays untouched
print(df.shape)                                    # .shape: (rows, columns)
print(df.head(10))                                 # .head(10): first 10 rows
df.info()                                          # .info(): column types + non-null counts

# %% Step 1: clean column names (habit for every project)
# .str.strip(): removes spaces at the ends; .str.lower(): small letters; .str.replace(a, b): swaps text a for b.
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns.tolist())                         # .columns: names; .tolist(): plain list

# %% Step 2: exact duplicate rows
print("duplicates:", df.duplicated().sum())        # .duplicated(): True for repeated rows; .sum(): counts them
print(df[df.duplicated(keep=False)])               # keep=False: mark every copy, including the first
df = df.drop_duplicates()                          # .drop_duplicates(): removes repeated rows (keeps first)
print(df.shape)

# %% Step 3: whitespace and letter case in text columns
df["customer_name"] = df["customer_name"].str.strip().str.title()   # .str.title(): Capital First Letters
df["city"] = df["city"].str.strip().str.title()
df["status"] = df["status"].str.strip().str.lower()
df["payment_method"] = df["payment_method"].str.strip().str.title()
print(df["customer_name"].head(3).tolist())
print(df["status"].value_counts())                 # .value_counts(): how many times each value appears
print(df["payment_method"].value_counts())

# %% Step 4: prices are text like "$1,200.00"
print(df["unit_price"].dtype)                      # .dtype: the data type (object = text)
df["unit_price"] = (
    df["unit_price"]
    .str.replace("$", "", regex=False)             # regex=False: treat "$" as plain text
    .str.replace(",", "", regex=False)
    .astype(float)                                 # .astype(float): change to decimal numbers
)
print(df["unit_price"].describe())                 # .describe(): count, mean, min, max...

# %% Step 5: dates in different formats
# pd.to_datetime(): turns text into real dates; format="mixed": each value may have its own format.
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")
print(df["order_date"].dtype)
print(df["order_date"].min(), df["order_date"].max())    # earliest and latest date

# %% Step 6: missing values (look first, then decide per column)
print(df.isna().sum())                             # .isna(): True where missing; counts per column
df["city"] = df["city"].fillna("Unknown")          # .fillna(x): replaces missing with x
df["discount"] = df["discount"].fillna(0.0)
df["rating"] = df["rating"].fillna(df["rating"].median())   # .median(): middle value
# unit_price missing: fill with typical price of the same product
# .groupby("product"): splits rows by product; .transform("median"): each group's median, lined up with every row.
df["unit_price"] = df["unit_price"].fillna(
    df.groupby("product")["unit_price"].transform("median")
)
print(df.isna().sum())

# %% Step 7: impossible or extreme values
print(df[df["quantity"] <= 0])                # a return, negative quantity; test in [] keeps matching rows
print(df["quantity"].describe())
q1, q3 = df["quantity"].quantile([0.25, 0.75])   # .quantile(): value below which that share of rows fall (25% and 75%)
iqr = q3 - q1                                 # IQR: the spread of the middle half of the data
upper = q3 + 1.5 * iqr                        # common rule for the "too big" limit
print("outlier limit:", upper)
print(df[df["quantity"] > upper][["order_id", "product", "quantity"]])   # [[a, b]]: pick columns

df["is_return"] = df["quantity"] < 0                  # < gives True/False for each row
df["quantity"] = df["quantity"].clip(upper=upper)     # .clip(upper=x): cap extreme values at x
df = df[df["quantity"] != 0]                          # != means "not equal"; drops zero rows

# %% Step 8: right data types
df["order_id"] = df["order_id"].astype(int)           # .astype(int): change to whole numbers
df["quantity"] = df["quantity"].round().astype(int)   # .round(): nearest whole number
df["rating"] = df["rating"].astype(int)
for column in ["category", "payment_method", "status", "city"]:
    df[column] = df[column].astype("category")        # "category": saves memory for text that repeats
df.info()

# %% Step 9: new useful columns
df["gross"] = df["quantity"] * df["unit_price"]       # * multiplies row by row
df["net_revenue"] = df["gross"] * (1 - df["discount"])
# .dt: date tools; .to_period("M"): month; .astype(str): to text.
df["month"] = df["order_date"].dt.to_period("M").astype(str)
df["weekday"] = df["order_date"].dt.day_name()        # .dt.day_name(): Monday, Tuesday...
print(df[["order_id", "gross", "net_revenue", "month", "weekday"]].head())

# %% Step 10: sanity checks (stop if something is still wrong)
# assert test, "message": stops the program with the message if the test is False.
assert df["order_id"].is_unique, "order ids should be unique"    # .is_unique: no repeats
assert df["unit_price"].notna().all()                 # .notna(): True where present; .all(): True if every item is True
assert df["discount"].between(0, 1).all()             # .between(0, 1): True if from 0 to 1
print("checks passed")

# %% Step 11: save the clean file
out = DATA / "output"                                 # path / "name": adds a folder name to a path
out.mkdir(exist_ok=True)                              # .mkdir(): creates the folder; exist_ok=True: no error if there
df.sort_values("order_id").to_csv(out / "sales_clean.csv", index=False)   # .sort_values(): order rows; .to_csv(): save as CSV; index=False: skip row numbers
print(pd.read_csv(out / "sales_clean.csv").head())

# %% Compare before and after
print(raw.shape, "->", df.shape)
print(raw.dtypes)                                     # .dtypes: data type of each column
print(df.dtypes)

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# (nothing rare here, everything above is core)
