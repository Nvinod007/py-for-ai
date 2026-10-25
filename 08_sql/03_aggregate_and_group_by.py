# Summaries: COUNT, SUM, AVG, GROUP BY, HAVING.
# Each line has a short comment saying WHAT it is.

import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
# sqlite3.connect(file): opens (or creates) the database file; conn is our open connection.
conn = sqlite3.connect(DATA / "output" / "shop.db")


# q = small helper: runs SQL text and returns the result as a pandas table.
def q(sql, params=()):
    # read_sql_query(sql, conn, params=...): runs the SQL on the connection; params fill the ? marks safely.
    return pd.read_sql_query(sql, conn, params=params)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Aggregate functions
# Aggregates squash many rows into one value: COUNT = how many, SUM = total, AVG = average, MIN = smallest, MAX = biggest.
print(q("""
    SELECT COUNT(*) AS people, SUM(salary) AS total, AVG(salary) AS average,
           MIN(salary) AS lowest, MAX(salary) AS highest
    FROM employees
"""))
# COUNT(DISTINCT col): number of different values.
print(q("SELECT COUNT(DISTINCT department) AS departments FROM employees"))
# COUNT(col) counts only rows where col is not empty.
print(q("SELECT COUNT(rating) AS rated, COUNT(*) AS all_rows FROM orders"))   # COUNT(col) skips NULL

# %% GROUP BY
# GROUP BY col: makes one row per different value, so aggregates work per group.
print(q("SELECT department, COUNT(*) AS people FROM employees GROUP BY department"))
# Same idea with more: ROUND(x) rounds, ORDER BY avg_salary DESC sorts biggest first (can sort by a new name).
print(q("""
    SELECT department, ROUND(AVG(salary)) AS avg_salary, MAX(salary) AS top
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
"""))
# GROUP BY a, b: one row per combination.
print(q("SELECT department, gender, COUNT(*) AS n FROM employees GROUP BY department, gender"))

# %% HAVING filters groups (WHERE filters rows BEFORE grouping)
# HAVING: filters whole groups after grouping (WHERE can't use COUNT).
print(q("""
    SELECT department, COUNT(*) AS people
    FROM employees
    GROUP BY department
    HAVING COUNT(*) >= 6
"""))
# WHERE age > 30 drops rows first, then groups are made, then HAVING drops groups.
print(q("""
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    WHERE age > 30
    GROUP BY department
    HAVING AVG(salary) > 80000
"""))

# %% Revenue per category from orders
# Revenue = quantity * price * (1 - discount); COALESCE(discount, 0) treats missing discount as 0.
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
# GROUP BY month: groups by the name given in SELECT; strftime('%Y-%m', date) = year-month text.
print(q("""
    SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS orders
    FROM orders
    GROUP BY month
    ORDER BY month
"""))

# %% Order of a query (the order SQL is READ, not run):
# SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT
# The order SQL RUNS: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Percentages
# A (SELECT COUNT(*) ...) inside brackets is a subquery giving one number (total people); 100.0 * part / total = percent.
print(q("""
    SELECT department,
           COUNT(*) AS people,
           ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM employees), 1) AS share_pct
    FROM employees
    GROUP BY department
"""))

# %% Conditional counts
# CASE WHEN ... THEN 1 ELSE 0 END turns a test into 1/0, so SUM counts matches.
print(q("""
    SELECT department,
           SUM(CASE WHEN remote = 1 THEN 1 ELSE 0 END) AS remote_people,
           SUM(remote) AS same_thing
    FROM employees
    GROUP BY department
"""))

# %% Join text of a group
# GROUP_CONCAT(col, separator): join all values of a group into one text.
print(q("SELECT department, GROUP_CONCAT(name, ', ') AS people FROM employees GROUP BY department LIMIT 2"))

conn.close()
