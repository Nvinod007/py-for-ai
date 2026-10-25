# SQL = the language for asking questions of databases. SQLite is built into Python.
# We load the course CSV files into a real database file, then query it.

import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
DB = DATA / "output" / "shop.db"
DB.parent.mkdir(exist_ok=True)

# %% Build the database from the CSV files (run this once)
sales = pd.read_csv(DATA / "01_sales_messy.csv").drop_duplicates()
sales["unit_price"] = sales["unit_price"].str.replace(r"[$,]", "", regex=True).astype(float)
sales["order_date"] = pd.to_datetime(sales["order_date"], format="mixed").dt.strftime("%Y-%m-%d")
sales["customer_name"] = sales["customer_name"].str.strip().str.title()
sales["status"] = sales["status"].str.lower()
customers = pd.read_csv(DATA / "02_customers.csv")
employees = pd.read_csv(DATA / "03_employees.csv")
employees["remote"] = employees["remote"].astype(int)

with sqlite3.connect(DB) as conn:
    sales.to_sql("orders", conn, if_exists="replace", index=False)
    customers.to_sql("customers", conn, if_exists="replace", index=False)
    employees.to_sql("employees", conn, if_exists="replace", index=False)
print("database ready:", DB.name)

# %% Connect and run a query
conn = sqlite3.connect(DB)
cursor = conn.execute("SELECT * FROM customers LIMIT 3")
print([col[0] for col in cursor.description])       # column names
print(cursor.fetchall())

# %% Rows as dictionaries
conn.row_factory = sqlite3.Row
row = conn.execute("SELECT * FROM customers WHERE customer_id = 'C001'").fetchone()
print(dict(row))

# %% Helper: run SQL and get a DataFrame
def q(sql, params=()):
    return pd.read_sql_query(sql, conn, params=params)


print(q("SELECT * FROM employees LIMIT 3"))

# %% See what tables and columns exist
print(q("SELECT name FROM sqlite_master WHERE type = 'table'"))
print(q("PRAGMA table_info(orders)")[["name", "type"]])

# %% Safe queries: NEVER build SQL with f-strings (SQL injection)
name = "Alice Johnson"
print(q("SELECT order_id, product FROM orders WHERE customer_name = ?", (name,)))
bad = "x' OR '1'='1"
print(len(q("SELECT * FROM orders WHERE customer_name = ?", (bad,))), "rows (injection did nothing)")

# %% Count rows
print(q("SELECT COUNT(*) AS total_orders FROM orders"))

conn.close()
