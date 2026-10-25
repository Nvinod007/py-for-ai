# SQL and pandas together, plus indexes and query plans.
# Each line has a short comment saying WHAT it is.

import sqlite3
import time
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
# sqlite3.connect(file): opens the database file.
conn = sqlite3.connect(DATA / "output" / "shop.db")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% SQL for pulling data, pandas for analysis
# read_sql_query(sql, conn): run SQL and get the result as a pandas table.
df = pd.read_sql_query("SELECT * FROM employees", conn)
# groupby(col)[col2].mean(): average of col2 per group; round(): round numbers.
print(df.groupby("department")["salary"].mean().round())

# %% Same question, two ways
# Same question done by SQL: GROUP BY makes groups, AVG averages, ROUND rounds.
sql_answer = pd.read_sql_query(
    "SELECT department, ROUND(AVG(salary)) AS avg_salary FROM employees GROUP BY department", conn
)
# as_index=False keeps department as a normal column.
pandas_answer = df.groupby("department", as_index=False)["salary"].mean().round()
print(sql_answer)
print(pandas_answer)

# %% Parameters, and dates parsed for you
# params=(...): values for the ? mark; parse_dates=[col]: turn that text column into real dates; .dtypes shows column types.
print(pd.read_sql_query("SELECT * FROM orders WHERE category = ?", conn, params=("Furniture",),
                        parse_dates=["order_date"]).dtypes["order_date"])

# %% Write a DataFrame to a table
# agg(people=("employee_id", "count")): name a result column and count that column's rows per group.
summary = df.groupby("department", as_index=False).agg(people=("employee_id", "count"))
# to_sql(name, conn, if_exists="replace", index=False): save a table into the database, replacing an old one.
summary.to_sql("dept_summary", conn, if_exists="replace", index=False)
print(pd.read_sql_query("SELECT * FROM dept_summary", conn))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Big results in chunks
# chunksize=10: read results 10 rows at a time instead of all at once (saves memory).
total = 0
for chunk in pd.read_sql_query("SELECT * FROM employees", conn, chunksize=10):
    total += len(chunk)
print(total)

# %% Indexes: speed up lookups
# DROP TABLE IF EXISTS: delete the table if it exists.
conn.execute("DROP TABLE IF EXISTS big")
# np.arange(n): numbers 0..n-1; default_rng(0).random(n): n random decimals (seed 0 = same every time).
big = pd.DataFrame({"id": np.arange(300_000), "value": np.random.default_rng(0).random(300_000)})
# No if_exists given, so it just creates the table.
big.to_sql("big", conn, index=False)

# time.perf_counter(): a precise clock, used to measure how long lookups take.
def timed_lookup():
    start = time.perf_counter()
    for key in range(0, 300_000, 15_000):
        # fetchall(): read all result rows (forces the query to finish).
        conn.execute("SELECT * FROM big WHERE id = ?", (key,)).fetchall()
    return time.perf_counter() - start

# Time lookups with no index first.
before = timed_lookup()
# CREATE INDEX: builds a lookup shortcut on that column.
conn.execute("CREATE INDEX idx_big_id ON big(id)")
# Time again with the index.
after = timed_lookup()
print(f"without index {before:.4f}s, with index {after:.4f}s")

# %% See how SQLite runs a query
# EXPLAIN QUERY PLAN: asks SQLite how it will run the query (scan everything or use an index).
for row in conn.execute("EXPLAIN QUERY PLAN SELECT * FROM big WHERE id = 5"):
    print(row[-1])                       # SEARCH ... USING INDEX means the index is used
# DROP TABLE: delete the table.
conn.execute("DROP TABLE big")

# %% When to use what
# Data lives in a database / too big for memory  -> SQL (filter and summarize there first)
# Exploring, charts, ML                          -> pandas
# Production apps                                -> SQL + an ORM like SQLAlchemy
# Next databases to know: PostgreSQL (the standard), DuckDB (SQL on CSV/parquet files)

# commit(): save the changes.
conn.commit()
conn.close()
