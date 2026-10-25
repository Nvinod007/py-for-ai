# Queries inside queries. CTEs (WITH) make long queries readable.

import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
conn = sqlite3.connect(DATA / "output" / "shop.db")


def q(sql, params=()):
    return pd.read_sql_query(sql, conn, params=params)


# %% Subquery in WHERE
print(q("SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)"))

print(q("""
    SELECT name FROM employees
    WHERE department IN (SELECT department FROM employees GROUP BY department HAVING AVG(salary) > 85000)
"""))

# %% EXISTS
print(q("""
    SELECT c.name FROM customers c
    WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'returned')
"""))

# %% Subquery in FROM
print(q("""
    SELECT department, ROUND(avg_salary) AS avg_salary
    FROM (SELECT department, AVG(salary) AS avg_salary FROM employees GROUP BY department)
    WHERE avg_salary > 70000
"""))

# %% Correlated subquery: compare each person to their own department
print(q("""
    SELECT e.name, e.department, e.salary
    FROM employees e
    WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE department = e.department)
    ORDER BY e.department, e.salary DESC
    LIMIT 8
"""))

# %% CTE: name a step, then use it
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

# %% Several CTEs, step by step
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
print(q("""
    WITH RECURSIVE numbers(n) AS (
        SELECT 1
        UNION ALL
        SELECT n + 1 FROM numbers WHERE n < 5
    )
    SELECT n, n * n AS square FROM numbers
"""))

conn.close()
