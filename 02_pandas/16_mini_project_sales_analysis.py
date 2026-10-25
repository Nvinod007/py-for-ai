# Mini project: clean the messy sales file, then answer business questions.
# Each line has a short comment saying WHAT the function is.
# Cleaning steps are explained in 07_cleaning_messy_sales_walkthrough.py.

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

from pathlib import Path

import pandas as pd

# Path(...).exists(): True if the folder exists. Path / "file" joins a folder and a file name.
DATA = Path("data") if Path("data").exists() else Path("../data")


# def name(): a reusable block of code; return gives back the result.
def load_clean_sales():
    # pd.read_csv(file): loads a CSV file. .drop_duplicates(): removes repeated rows.
    df = pd.read_csv(DATA / "01_sales_messy.csv").drop_duplicates()
    # .str: text tools for a column. .str.strip(): cuts spaces at the ends. .str.title(): Capitalizes Each Word.
    df["customer_name"] = df["customer_name"].str.strip().str.title()
    # .fillna(x): replaces missing values with x.
    df["city"] = df["city"].str.strip().str.title().fillna("Unknown")
    # .str.lower(): small letters.
    df["status"] = df["status"].str.lower()
    df["payment_method"] = df["payment_method"].str.title()
    # .str.replace(pattern, new, regex=True): replaces text matching the pattern ([$,] = $ or comma). .astype(float): converts to decimal numbers.
    df["unit_price"] = df["unit_price"].str.replace(r"[$,]", "", regex=True).astype(float)
    # .groupby(col)[col2].transform("median"): middle value per group, repeated on each row, used to fill gaps.
    df["unit_price"] = df["unit_price"].fillna(df.groupby("product")["unit_price"].transform("median"))
    # pd.to_datetime(col, format="mixed"): converts text to dates, each may look different.
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")
    # Missing discount means 0.
    df["discount"] = df["discount"].fillna(0)
    # df[test]: keep rows where the test is True. & means AND; each test needs ( ).
    df = df[(df["quantity"] > 0) & (df["quantity"] < 100)]
    # New column: quantity x price x (1 - discount).
    df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
    # .dt.to_period("M"): the dates as whole months. .dt works on date columns.
    df["month"] = df["order_date"].dt.to_period("M")
    return df


# Calling the function runs the cleaning steps.
sales = load_clean_sales()
delivered = sales[sales["status"] == "delivered"]
# .shape: (rows, columns).
print(sales.shape, delivered.shape)

# %% Q1: total revenue?
# round(x, 2): rounds to 2 decimals. .sum(): total.
print(round(delivered["revenue"].sum(), 2))

# %% Q2: revenue by category, biggest first
# df.groupby(col)[col2].sum(): total per group. .sort_values(ascending=False): biggest first. .round(0): whole numbers.
print(delivered.groupby("category")["revenue"].sum().sort_values(ascending=False).round(0))

# %% Q3: revenue per month and growth
# Total revenue per month.
monthly = delivered.groupby("month")["revenue"].sum()
# pd.DataFrame({name: values}): builds a table. .pct_change(): percent change from the previous row.
print(pd.DataFrame({"revenue": monthly.round(0), "growth_%": (monthly.pct_change() * 100).round(1)}))

# %% Q4: top 5 customers
# .nlargest(5): the 5 biggest values.
print(delivered.groupby("customer_name")["revenue"].sum().nlargest(5).round(0))

# %% Q5: which city sells the most Electronics?
# Keep only Electronics rows.
electronics = delivered[delivered["category"] == "Electronics"]
print(electronics.groupby("city")["revenue"].sum().sort_values(ascending=False).round(0))

# %% Q6: favourite payment method share
# .value_counts(normalize=True): share of each value (0 to 1).
print(delivered["payment_method"].value_counts(normalize=True).round(2))

# %% Q7: average rating per category
# .mean(): average.
print(delivered.groupby("category")["rating"].mean().round(2))

# %% Q8: does a bigger discount mean a bigger order?
# df.corr(): how strongly columns move together (-1 to 1).
print(delivered[["discount", "revenue", "quantity"]].corr().round(2))

# %% Q9: best-selling product by units
# .head(5): first 5 rows.
print(delivered.groupby("product")["quantity"].sum().sort_values(ascending=False).head(5))

# %% Q10: orders and revenue by weekday
# df.assign(day=...): adds a column. .dt.day_name(): weekday name. .agg(name=(col, function)): named summaries; count = rows.
by_day = delivered.assign(day=delivered["order_date"].dt.day_name()).groupby("day").agg(
    orders=("order_id", "count"), revenue=("revenue", "sum")
)
print(by_day.round(0))

# %% Your turn
# 1. Which customers ordered more than once?
# 2. What share of orders were returned or cancelled?
# 3. Which month had the highest average order value?

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# (nothing rare here, everything above is core)
