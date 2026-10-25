# JOIN = combine tables using a shared key. Same idea as pandas merge.
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

# %% INNER JOIN: only rows that match in both
# AS o: short nickname for a table. INNER JOIN ... ON: link rows where the key columns match; rows without a match are dropped.
print(q("""
    SELECT o.order_id, o.customer_id, c.name, c.tier, o.product
    FROM orders AS o
    INNER JOIN customers AS c ON c.customer_id = o.customer_id
    LIMIT 5
"""))

# %% LEFT JOIN: every order, even without a customer record
# LEFT JOIN: keep ALL rows of the left table; missing matches become NULL. WHERE c.customer_id IS NULL then finds the unmatched ones.
print(q("""
    SELECT o.order_id, o.customer_id, c.tier
    FROM orders AS o
    LEFT JOIN customers AS c ON c.customer_id = o.customer_id
    WHERE c.customer_id IS NULL
"""))

# %% Customers who never ordered (LEFT JOIN + IS NULL)
# Start from customers, LEFT JOIN orders, keep the NULL ones = customers with no orders.
print(q("""
    SELECT c.customer_id, c.name
    FROM customers AS c
    LEFT JOIN orders AS o ON o.customer_id = c.customer_id
    WHERE o.order_id IS NULL
"""))

# %% Aggregate over a join
# JOIN alone = INNER JOIN. COUNT/SUM per group after joining; GROUP BY c.tier = one row per tier.
print(q("""
    SELECT c.tier,
           COUNT(*) AS orders,
           ROUND(SUM(o.quantity * o.unit_price), 0) AS gross
    FROM orders AS o
    JOIN customers AS c ON c.customer_id = o.customer_id
    GROUP BY c.tier
    ORDER BY gross DESC
"""))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Join a table to itself (employees in the same department)
# Self join: the same table twice under nicknames a and b; a.employee_id < b.employee_id avoids pairing a person with themselves or twice.
print(q("""
    SELECT a.name AS person, b.name AS colleague, a.department
    FROM employees AS a
    JOIN employees AS b ON a.department = b.department AND a.employee_id < b.employee_id
    WHERE a.department = 'HR'
"""))

# %% Join three tables
# Nicknames can skip AS (orders o). != means not equal; compares two columns from joined tables.
print(q("""
    SELECT c.name, c.city AS home_city, o.city AS shipped_to, o.product
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE c.city != o.city
    LIMIT 5
"""))

# %% UNION: stack results of two queries
# UNION: stacks two results into one list (columns must match) and removes duplicates; 'employee' AS kind adds a fixed label column.
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
