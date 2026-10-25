# Mini project: clean the messy sales file, then answer business questions.
# Cleaning steps are explained in 07_cleaning_messy_sales_walkthrough.py.

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")


def load_clean_sales():
    df = pd.read_csv(DATA / "01_sales_messy.csv").drop_duplicates()
    df["customer_name"] = df["customer_name"].str.strip().str.title()
    df["city"] = df["city"].str.strip().str.title().fillna("Unknown")
    df["status"] = df["status"].str.lower()
    df["payment_method"] = df["payment_method"].str.title()
    df["unit_price"] = df["unit_price"].str.replace(r"[$,]", "", regex=True).astype(float)
    df["unit_price"] = df["unit_price"].fillna(df.groupby("product")["unit_price"].transform("median"))
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")
    df["discount"] = df["discount"].fillna(0)
    df = df[(df["quantity"] > 0) & (df["quantity"] < 100)]
    df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
    df["month"] = df["order_date"].dt.to_period("M")
    return df


sales = load_clean_sales()
delivered = sales[sales["status"] == "delivered"]
print(sales.shape, delivered.shape)

# %% Q1: total revenue?
print(round(delivered["revenue"].sum(), 2))

# %% Q2: revenue by category, biggest first
print(delivered.groupby("category")["revenue"].sum().sort_values(ascending=False).round(0))

# %% Q3: revenue per month and growth
monthly = delivered.groupby("month")["revenue"].sum()
print(pd.DataFrame({"revenue": monthly.round(0), "growth_%": (monthly.pct_change() * 100).round(1)}))

# %% Q4: top 5 customers
print(delivered.groupby("customer_name")["revenue"].sum().nlargest(5).round(0))

# %% Q5: which city sells the most Electronics?
electronics = delivered[delivered["category"] == "Electronics"]
print(electronics.groupby("city")["revenue"].sum().sort_values(ascending=False).round(0))

# %% Q6: favourite payment method share
print(delivered["payment_method"].value_counts(normalize=True).round(2))

# %% Q7: average rating per category
print(delivered.groupby("category")["rating"].mean().round(2))

# %% Q8: does a bigger discount mean a bigger order?
print(delivered[["discount", "revenue", "quantity"]].corr().round(2))

# %% Q9: best-selling product by units
print(delivered.groupby("product")["quantity"].sum().sort_values(ascending=False).head(5))

# %% Q10: orders and revenue by weekday
by_day = delivered.assign(day=delivered["order_date"].dt.day_name()).groupby("day").agg(
    orders=("order_id", "count"), revenue=("revenue", "sum")
)
print(by_day.round(0))

# %% Your turn
# 1. Which customers ordered more than once?
# 2. What share of orders were returned or cancelled?
# 3. Which month had the highest average order value?
