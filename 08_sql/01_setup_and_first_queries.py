# SQL = the language for asking questions of databases. SQLite is built into Python.
# We load the course CSV files into a real database file, then query it.
# Each line has a short comment saying WHAT it is.

import sqlite3
from pathlib import Path

import pandas as pd

# Path(...).exists(): True if the folder exists; picks whichever data folder is found.
DATA = Path("data") if Path("data").exists() else Path("../data")
DB = DATA / "output" / "shop.db"
# mkdir(exist_ok=True): make the folder, no error if it is already there.
DB.parent.mkdir(exist_ok=True)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Build the database from the CSV files (run this once)
# read_csv: load a CSV file into a table. drop_duplicates(): remove repeated rows.
sales = pd.read_csv(DATA / "01_sales_messy.csv").drop_duplicates()
# str.replace(regex, ""): delete $ and commas; astype(float): turn text into decimal numbers.
sales["unit_price"] = sales["unit_price"].str.replace(r"[$,]", "", regex=True).astype(float)
# to_datetime(format="mixed"): read dates written in different styles; strftime: write them as YYYY-MM-DD text.
sales["order_date"] = pd.to_datetime(sales["order_date"], format="mixed").dt.strftime("%Y-%m-%d")
# str.strip(): cut spaces at the ends; str.title(): Capitalize Each Word.
sales["customer_name"] = sales["customer_name"].str.strip().str.title()
# str.lower(): make text lowercase.
sales["status"] = sales["status"].str.lower()
customers = pd.read_csv(DATA / "02_customers.csv")
employees = pd.read_csv(DATA / "03_employees.csv")
# astype(int): True/False becomes 1/0 (SQLite has no True/False).
employees["remote"] = employees["remote"].astype(int)

# with ...: opens the connection and saves/closes it automatically at the end.
with sqlite3.connect(DB) as conn:
    # to_sql(name, conn, if_exists="replace", index=False): write a table into the database; replace = overwrite old one; index=False = skip the row numbers.
    sales.to_sql("orders", conn, if_exists="replace", index=False)
    customers.to_sql("customers", conn, if_exists="replace", index=False)
    employees.to_sql("employees", conn, if_exists="replace", index=False)
print("database ready:", DB.name)

# %% Connect and run a query
# sqlite3.connect(file): opens the database file; conn is our open connection.
conn = sqlite3.connect(DB)
# conn.execute(sql): runs SQL. SELECT * = all columns; FROM customers = which table; LIMIT 3 = only 3 rows.
cursor = conn.execute("SELECT * FROM customers LIMIT 3")
# cursor.description: info about the result columns; col[0] is each column's name.
print([col[0] for col in cursor.description])       # column names
# fetchall(): get every result row as a list of tuples.
print(cursor.fetchall())

# %% Helper: run SQL and get a DataFrame
# q = small helper: runs SQL text and returns a pandas table.
def q(sql, params=()):
    # read_sql_query(sql, conn, params=...): runs SQL and gives a table; params fill the ? marks safely.
    return pd.read_sql_query(sql, conn, params=params)


print(q("SELECT * FROM employees LIMIT 3"))

# %% Safe queries: NEVER build SQL with f-strings (SQL injection)
# A ? in SQL is a placeholder; the value is passed separately so it can never be run as SQL.
name = "Alice Johnson"
# (name,): a tuple holding the value that replaces the ?.
print(q("SELECT order_id, product FROM orders WHERE customer_name = ?", (name,)))
# A sneaky input that tries to trick the query; with ? it is treated as plain text.
bad = "x' OR '1'='1"
print(len(q("SELECT * FROM orders WHERE customer_name = ?", (bad,))), "rows (injection did nothing)")

# %% Count rows
# COUNT(*): how many rows; AS total_orders: gives the result column a name.
print(q("SELECT COUNT(*) AS total_orders FROM orders"))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Rows as dictionaries
# row_factory = sqlite3.Row: rows act like dictionaries (look up by column name).
conn.row_factory = sqlite3.Row
# WHERE customer_id = 'C001': keep only matching rows; fetchone(): get just the first row.
row = conn.execute("SELECT * FROM customers WHERE customer_id = 'C001'").fetchone()
# dict(row): turn the row into a normal dictionary.
print(dict(row))

# %% See what tables and columns exist
# sqlite_master: SQLite's built-in list of everything in the database; type = 'table' keeps only tables.
print(q("SELECT name FROM sqlite_master WHERE type = 'table'"))
# PRAGMA table_info(table): SQLite command that lists a table's columns and types.
print(q("PRAGMA table_info(orders)")[["name", "type"]])

# close(): shut the database connection.
conn.close()
