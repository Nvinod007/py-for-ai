# Summaries: COUNT, SUM, AVG, GROUP BY, HAVING.

import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
conn = sqlite3.connect(DATA / "output" / "shop.db")


def q(sql, params=()):
    return pd.read_sql_query(sql, conn, params=params)


# %% Aggregate functions
print(q("""
    SELECT COUNT(*) AS people, SUM(salary) AS total, AVG(salary) AS average,
           MIN(salary) AS lowest, MAX(salary) AS highest
    FROM employees
"""))
print(q("SELECT COUNT(DISTINCT department) AS departments FROM employees"))
print(q("SELECT COUNT(rating) AS rated, COUNT(*) AS all_rows FROM orders"))   # COUNT(col) skips NULL

# %% GROUP BY
print(q("SELECT department, COUNT(*) AS people FROM employees GROUP BY department"))
print(q("""
    SELECT department, ROUND(AVG(salary)) AS avg_salary, MAX(salary) AS top
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
"""))
print(q("SELECT department, gender, COUNT(*) AS n FROM employees GROUP BY department, gender"))

# %% HAVING filters groups (WHERE filters rows BEFORE grouping)
print(q("""
    SELECT department, COUNT(*) AS people
    FROM employees
    GROUP BY department
    HAVING COUNT(*) >= 6
"""))
print(q("""
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    WHERE age > 30
    GROUP BY department
    HAVING AVG(salary) > 80000
"""))

# %% Revenue per category from orders
print(q("""
    SELECT category,
           COUNT(*) AS orders,
           SUM(quantity) AS units,
           ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount, 0))), 2) AS revenue
    FROM orders
    WHERE status = 'delivered' AND quantity > 0
    GROUP BY category
    ORDER BY revenue DESC
"""))

# %% By month
print(q("""
    SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS orders
    FROM orders
    GROUP BY month
    ORDER BY month
"""))

# %% Percentages
print(q("""
    SELECT department,
           COUNT(*) AS people,
           ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM employees), 1) AS share_pct
    FROM employees
    GROUP BY department
"""))

# %% Conditional counts
print(q("""
    SELECT department,
           SUM(CASE WHEN remote = 1 THEN 1 ELSE 0 END) AS remote_people,
           SUM(remote) AS same_thing
    FROM employees
    GROUP BY department
"""))

# %% Join text of a group
print(q("SELECT department, GROUP_CONCAT(name, ', ') AS people FROM employees GROUP BY department LIMIT 2"))

# %% Order of a query (the order SQL is READ, not run):
# SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT
# The order SQL RUNS: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT

conn.close()
