# Queries inside queries. CTEs (WITH) make long queries readable.
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

# %% Subquery in WHERE
# Subquery: a SELECT in brackets that gives a value (here the average) for the outer query to use.
print(q("SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)"))

# Subquery can give a list too: IN (SELECT ...) matches departments whose average is high.
print(q("""
    SELECT name FROM employees
    WHERE department IN (SELECT department FROM employees GROUP BY department HAVING AVG(salary) > 85000)
"""))

# %% Subquery in FROM
# Subquery in FROM: the inner SELECT acts like a temporary table that the outer query reads.
print(q("""
    SELECT department, ROUND(avg_salary) AS avg_salary
    FROM (SELECT department, AVG(salary) AS avg_salary FROM employees GROUP BY department)
    WHERE avg_salary > 70000
"""))

# %% CTE: name a step, then use it
# WITH name AS (...): CTE = a named temporary result, defined first and used like a table below.
print(q("""
    WITH dept_avg AS (
        SELECT department, AVG(salary) AS avg_salary
        FROM employees
        GROUP BY department
    )
    SELECT e.name, e.department, e.salary, ROUND(d.avg_salary) AS dept_avg
    FROM employees e
    JOIN dept_avg d ON d.department = e.department
    WHERE e.salary > d.avg_salary
    LIMIT 5
"""))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% EXISTS
# EXISTS (SELECT ...): true if the inner query finds at least one row; SELECT 1 just means 'something'.
print(q("""
    SELECT c.name FROM customers c
    WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'returned')
"""))

# %% Correlated subquery: compare each person to their own department
# Correlated subquery: the inner query uses e.department from the outer row, so it re-runs per row.
print(q("""
    SELECT e.name, e.department, e.salary
    FROM employees e
    WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE department = e.department)
    ORDER BY e.department, e.salary DESC
    LIMIT 8
"""))

# %% Several CTEs, step by step
# Several CTEs separated by commas; each can use the ones before it.
print(q("""
    WITH clean_orders AS (
        SELECT customer_id, quantity * unit_price * (1 - COALESCE(discount, 0)) AS revenue
        FROM orders
        WHERE status = 'delivered' AND quantity > 0 AND unit_price IS NOT NULL
    ),
    per_customer AS (
        SELECT customer_id, SUM(revenue) AS total
        FROM clean_orders
        GROUP BY customer_id
    )
    SELECT c.name, c.tier, ROUND(p.total, 0) AS total
    FROM per_customer p
    JOIN customers c ON c.customer_id = p.customer_id
    ORDER BY total DESC
    LIMIT 5
"""))

# %% Recursive CTE (counting, trees, org charts)
# WITH RECURSIVE: a CTE that calls itself; start row (SELECT 1), then UNION ALL adds next rows until the WHERE stops it.
print(q("""
    WITH RECURSIVE numbers(n) AS (
        SELECT 1
        UNION ALL
        SELECT n + 1 FROM numbers WHERE n < 5
    )
    SELECT n, n * n AS square FROM numbers
"""))

conn.close()
