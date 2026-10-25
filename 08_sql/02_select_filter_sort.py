# SELECT, WHERE, ORDER BY, LIMIT: the core of SQL.
# Run 01_setup_and_first_queries.py first to create the database.

import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
conn = sqlite3.connect(DATA / "output" / "shop.db")


def q(sql, params=()):
    return pd.read_sql_query(sql, conn, params=params)


# %% Pick columns
print(q("SELECT name, department, salary FROM employees LIMIT 5"))
print(q("SELECT * FROM employees LIMIT 2"))
print(q("SELECT DISTINCT department FROM employees"))
print(q("SELECT name AS employee, salary * 12 AS yearly_if_monthly FROM employees LIMIT 3"))

# %% WHERE: filter rows
print(q("SELECT name, salary FROM employees WHERE salary > 100000"))
print(q("SELECT name FROM employees WHERE department = 'HR'"))
print(q("SELECT name FROM employees WHERE department != 'HR' AND age < 30"))
print(q("SELECT name FROM employees WHERE department = 'HR' OR department = 'Finance'"))
print(q("SELECT name FROM employees WHERE NOT remote"))

# %% IN, BETWEEN, LIKE
print(q("SELECT name, department FROM employees WHERE department IN ('HR', 'Finance')"))
print(q("SELECT name, salary FROM employees WHERE salary BETWEEN 60000 AND 70000"))
print(q("SELECT name FROM employees WHERE name LIKE 'A%'"))         # starts with A
print(q("SELECT name FROM employees WHERE name LIKE '%an%'"))      # contains "an"
print(q("SELECT name FROM employees WHERE name LIKE '_ara%'"))     # _ = one character

# %% NULL needs IS NULL (never = NULL)
print(q("SELECT COUNT(*) AS missing_rating FROM orders WHERE rating IS NULL"))
print(q("SELECT COUNT(*) AS has_city FROM orders WHERE city IS NOT NULL"))
print(q("SELECT order_id, COALESCE(city, 'Unknown') AS city FROM orders WHERE city IS NULL"))

# %% ORDER BY and LIMIT
print(q("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3"))
print(q("SELECT name, department, salary FROM employees ORDER BY department, salary DESC LIMIT 6"))
print(q("SELECT name FROM employees ORDER BY name LIMIT 3 OFFSET 3"))    # page 2 of size 3

# %% Calculations and text functions
print(q("SELECT name, UPPER(name) AS up, LENGTH(name) AS len, SUBSTR(name, 1, 3) AS first3 FROM employees LIMIT 3"))
print(q("SELECT ROUND(salary / 12.0, 0) AS monthly FROM employees LIMIT 3"))
print(q("SELECT name || ' (' || department || ')' AS label FROM employees LIMIT 3"))
print(q("SELECT REPLACE(name, ' ', '_') AS slug FROM employees LIMIT 2"))
print(q("SELECT ABS(-5) AS a, MAX(3, 9) AS b, MIN(3, 9) AS c"))

# %% CASE: if / else in SQL
print(q("""
    SELECT name, salary,
           CASE WHEN salary >= 100000 THEN 'High'
                WHEN salary >= 70000  THEN 'Mid'
                ELSE 'Low' END AS band
    FROM employees LIMIT 6
"""))

# %% Dates (SQLite keeps dates as text YYYY-MM-DD)
print(q("SELECT order_id, order_date, strftime('%Y-%m', order_date) AS month FROM orders LIMIT 3"))
print(q("SELECT order_id FROM orders WHERE order_date >= '2024-04-01'"))
print(q("SELECT julianday('2024-03-15') - julianday('2024-01-01') AS days"))

conn.close()
