# JOIN = combine tables using a shared key. Same idea as pandas merge.

import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
conn = sqlite3.connect(DATA / "output" / "shop.db")


def q(sql, params=()):
    return pd.read_sql_query(sql, conn, params=params)


# %% INNER JOIN: only rows that match in both
print(q("""
    SELECT o.order_id, o.customer_id, c.name, c.tier, o.product
    FROM orders AS o
    INNER JOIN customers AS c ON c.customer_id = o.customer_id
    LIMIT 5
"""))

# %% LEFT JOIN: every order, even without a customer record
print(q("""
    SELECT o.order_id, o.customer_id, c.tier
    FROM orders AS o
    LEFT JOIN customers AS c ON c.customer_id = o.customer_id
    WHERE c.customer_id IS NULL
"""))

# %% Customers who never ordered (LEFT JOIN + IS NULL)
print(q("""
    SELECT c.customer_id, c.name
    FROM customers AS c
    LEFT JOIN orders AS o ON o.customer_id = c.customer_id
    WHERE o.order_id IS NULL
"""))

# %% Aggregate over a join
print(q("""
    SELECT c.tier,
           COUNT(*) AS orders,
           ROUND(SUM(o.quantity * o.unit_price), 0) AS gross
    FROM orders AS o
    JOIN customers AS c ON c.customer_id = o.customer_id
    GROUP BY c.tier
    ORDER BY gross DESC
"""))

# %% Join a table to itself (employees in the same department)
print(q("""
    SELECT a.name AS person, b.name AS colleague, a.department
    FROM employees AS a
    JOIN employees AS b ON a.department = b.department AND a.employee_id < b.employee_id
    WHERE a.department = 'HR'
"""))

# %% Join three tables
print(q("""
    SELECT c.name, c.city AS home_city, o.city AS shipped_to, o.product
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE c.city != o.city
    LIMIT 5
"""))

# %% UNION: stack results of two queries
print(q("""
    SELECT name, 'employee' AS kind FROM employees WHERE department = 'HR'
    UNION
    SELECT name, 'customer' FROM customers WHERE tier = 'Gold'
"""))
# UNION removes duplicates, UNION ALL keeps them

# %% Join types in one picture
# INNER   rows with a match on both sides
# LEFT    all left rows + matching right rows (else NULL)
# RIGHT   mirror of LEFT (SQLite supports it in new versions)
# FULL    all rows from both (SQLite 3.39+)
# CROSS   every pair of rows

conn.close()
