# Window functions: calculate across related rows WITHOUT collapsing them.
# GROUP BY gives one row per group. A window keeps every row.
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

# %% Rank inside a group
# func() OVER (...): a window function = calculation across related rows while keeping every row.
# PARTITION BY col: split rows into groups (like GROUP BY but rows stay); ORDER BY inside OVER: order within the group.
# RANK(): position, ties share a rank and leave gaps; DENSE_RANK(): ties share, no gaps; ROW_NUMBER(): unique 1,2,3.
print(q("""
    SELECT name, department, salary,
           RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rank_in_dept,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_no,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS overall_dense
    FROM employees
    ORDER BY department, rank_in_dept
    LIMIT 8
"""))

# %% Top 2 per department
# Trick: number rows per department in a subquery, then WHERE rn <= 2 keeps the top 2 of each.
print(q("""
    SELECT * FROM (
        SELECT name, department, salary,
               ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
        FROM employees
    )
    WHERE rn <= 2
    ORDER BY department, rn
"""))

# %% Group totals next to each row
# AVG/SUM(...) OVER (PARTITION BY ...): group average/total shown next to every row.
print(q("""
    SELECT name, department, salary,
           ROUND(AVG(salary) OVER (PARTITION BY department)) AS dept_avg,
           salary - ROUND(AVG(salary) OVER (PARTITION BY department)) AS vs_avg,
           ROUND(100.0 * salary / SUM(salary) OVER (PARTITION BY department), 1) AS pct_of_dept
    FROM employees
    LIMIT 6
"""))

# %% Running total
# SUM(...) OVER (ORDER BY ...): running total, adds up row by row in that order.
print(q("""
    SELECT order_date, order_id,
           ROUND(quantity * unit_price, 0) AS amount,
           ROUND(SUM(quantity * unit_price) OVER (ORDER BY order_date, order_id), 0) AS running_total
    FROM orders
    WHERE status = 'delivered' AND quantity > 0 AND unit_price IS NOT NULL
    LIMIT 6
"""))

# %% Previous and next rows (LAG / LEAD)
# LAG(col): the value from the previous row; (LEAD would be the next). WITH monthly AS (...) is a CTE: a named temporary result.
print(q("""
    WITH monthly AS (
        SELECT strftime('%Y-%m', order_date) AS month,
               ROUND(SUM(quantity * unit_price), 0) AS revenue
        FROM orders
        WHERE quantity > 0 AND unit_price IS NOT NULL AND quantity < 100
        GROUP BY month
    )
    SELECT month, revenue,
           LAG(revenue)  OVER (ORDER BY month) AS previous,
           revenue - LAG(revenue) OVER (ORDER BY month) AS change
    FROM monthly
"""))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Moving average (last 3 rows)
# ROWS BETWEEN 2 PRECEDING AND CURRENT ROW: window of this row and the 2 before it = moving average.
print(q("""
    SELECT employee_id, join_date, salary,
           ROUND(AVG(salary) OVER (ORDER BY join_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS moving_avg
    FROM employees
    ORDER BY join_date
    LIMIT 6
"""))

# %% First, last, and buckets
# FIRST_VALUE(col): first value in the window; NTILE(4): split rows into 4 equal buckets numbered 1-4.
print(q("""
    SELECT name, department, salary,
           FIRST_VALUE(name) OVER (PARTITION BY department ORDER BY salary DESC) AS top_earner,
           NTILE(4) OVER (ORDER BY salary) AS quartile
    FROM employees
    LIMIT 6
"""))

conn.close()
