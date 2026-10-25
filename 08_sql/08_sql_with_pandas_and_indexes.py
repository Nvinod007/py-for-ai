# SQL and pandas together, plus indexes and query plans.

import sqlite3
import time
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
conn = sqlite3.connect(DATA / "output" / "shop.db")

# %% SQL for pulling data, pandas for analysis
df = pd.read_sql_query("SELECT * FROM employees", conn)
print(df.groupby("department")["salary"].mean().round())

# %% Same question, two ways
sql_answer = pd.read_sql_query(
    "SELECT department, ROUND(AVG(salary)) AS avg_salary FROM employees GROUP BY department", conn
)
pandas_answer = df.groupby("department", as_index=False)["salary"].mean().round()
print(sql_answer)
print(pandas_answer)

# %% Parameters, and dates parsed for you
print(pd.read_sql_query("SELECT * FROM orders WHERE category = ?", conn, params=("Furniture",),
                        parse_dates=["order_date"]).dtypes["order_date"])

# %% Write a DataFrame to a table
summary = df.groupby("department", as_index=False).agg(people=("employee_id", "count"))
summary.to_sql("dept_summary", conn, if_exists="replace", index=False)
print(pd.read_sql_query("SELECT * FROM dept_summary", conn))

# %% Big results in chunks
total = 0
for chunk in pd.read_sql_query("SELECT * FROM employees", conn, chunksize=10):
    total += len(chunk)
print(total)

# %% Indexes: speed up lookups
conn.execute("DROP TABLE IF EXISTS big")
big = pd.DataFrame({"id": np.arange(300_000), "value": np.random.default_rng(0).random(300_000)})
big.to_sql("big", conn, index=False)

def timed_lookup():
    start = time.perf_counter()
    for key in range(0, 300_000, 15_000):
        conn.execute("SELECT * FROM big WHERE id = ?", (key,)).fetchall()
    return time.perf_counter() - start

before = timed_lookup()
conn.execute("CREATE INDEX idx_big_id ON big(id)")
after = timed_lookup()
print(f"without index {before:.4f}s, with index {after:.4f}s")

# %% See how SQLite runs a query
for row in conn.execute("EXPLAIN QUERY PLAN SELECT * FROM big WHERE id = 5"):
    print(row[-1])                       # SEARCH ... USING INDEX means the index is used
conn.execute("DROP TABLE big")

# %% When to use what
# Data lives in a database / too big for memory  -> SQL (filter and summarize there first)
# Exploring, charts, ML                          -> pandas
# Production apps                                -> SQL + an ORM like SQLAlchemy
# Next databases to know: PostgreSQL (the standard), DuckDB (SQL on CSV/parquet files)

conn.commit()
conn.close()
