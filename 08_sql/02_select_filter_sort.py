# SELECT, WHERE, ORDER BY, LIMIT: the core of SQL.
# Run 01_setup_and_first_queries.py first to create the database.
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

# %% Pick columns
# SELECT columns FROM table: choose which columns to show; LIMIT 5: only the first 5 rows.
print(q("SELECT name, department, salary FROM employees LIMIT 5"))
# SELECT *: every column.
print(q("SELECT * FROM employees LIMIT 2"))
# DISTINCT: remove repeated values.
print(q("SELECT DISTINCT department FROM employees"))
# AS: rename a column in the result; salary * 12 is a calculation done per row.
print(q("SELECT name AS employee, salary * 12 AS yearly_if_monthly FROM employees LIMIT 3"))

# %% WHERE: filter rows
# WHERE: keep only rows where the test is true (> bigger than).
print(q("SELECT name, salary FROM employees WHERE salary > 100000"))
# = equals (single = in SQL); text goes in single quotes.
print(q("SELECT name FROM employees WHERE department = 'HR'"))
# != not equal; AND: both tests must be true; < smaller than.
print(q("SELECT name FROM employees WHERE department != 'HR' AND age < 30"))
# OR: at least one test must be true.
print(q("SELECT name FROM employees WHERE department = 'HR' OR department = 'Finance'"))
# NOT: flips true/false (here: people who are not remote).
print(q("SELECT name FROM employees WHERE NOT remote"))

# %% IN, BETWEEN, LIKE
# IN (...): matches any value in the list.
print(q("SELECT name, department FROM employees WHERE department IN ('HR', 'Finance')"))
# BETWEEN a AND b: value from a to b, both included.
print(q("SELECT name, salary FROM employees WHERE salary BETWEEN 60000 AND 70000"))
# LIKE: match text patterns; % means any number of characters.
print(q("SELECT name FROM employees WHERE name LIKE 'A%'"))         # starts with A
# % on both sides: the text can be anywhere.
print(q("SELECT name FROM employees WHERE name LIKE '%an%'"))      # contains "an"
# _ means exactly one character.
print(q("SELECT name FROM employees WHERE name LIKE '_ara%'"))     # _ = one character

# %% NULL needs IS NULL (never = NULL)
# IS NULL: tests for empty/missing values (= NULL never works); COUNT(*): number of rows.
print(q("SELECT COUNT(*) AS missing_rating FROM orders WHERE rating IS NULL"))
# IS NOT NULL: value is present.
print(q("SELECT COUNT(*) AS has_city FROM orders WHERE city IS NOT NULL"))
# COALESCE(a, b): use a, or b if a is empty.
print(q("SELECT order_id, COALESCE(city, 'Unknown') AS city FROM orders WHERE city IS NULL"))

# %% ORDER BY and LIMIT
# ORDER BY: sort the rows; DESC = biggest first (default is smallest first).
print(q("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3"))
# ORDER BY a, b: sort by a, then by b inside ties.
print(q("SELECT name, department, salary FROM employees ORDER BY department, salary DESC LIMIT 6"))
# OFFSET 3: skip the first 3 rows (used for paging).
print(q("SELECT name FROM employees ORDER BY name LIMIT 3 OFFSET 3"))    # page 2 of size 3

# %% CASE: if / else in SQL
# CASE WHEN ... THEN ... ELSE ... END: SQL's if/elif/else, picks a label per row (first true wins).
print(q("""
    SELECT name, salary,
           CASE WHEN salary >= 100000 THEN 'High'
                WHEN salary >= 70000  THEN 'Mid'
                ELSE 'Low' END AS band
    FROM employees LIMIT 6
"""))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Calculations and text functions
# UPPER: capital letters; LENGTH: number of characters; SUBSTR(text, start, count): cut part of the text.
print(q("SELECT name, UPPER(name) AS up, LENGTH(name) AS len, SUBSTR(name, 1, 3) AS first3 FROM employees LIMIT 3"))
# ROUND(number, digits): round to that many decimals; 12.0 makes it decimal division.
print(q("SELECT ROUND(salary / 12.0, 0) AS monthly FROM employees LIMIT 3"))
# ||: join pieces of text together.
print(q("SELECT name || ' (' || department || ')' AS label FROM employees LIMIT 3"))
# REPLACE(text, old, new): swap text for other text.
print(q("SELECT REPLACE(name, ' ', '_') AS slug FROM employees LIMIT 2"))
# ABS: remove minus sign; MAX(a, b)/MIN(a, b): bigger/smaller of two values.
print(q("SELECT ABS(-5) AS a, MAX(3, 9) AS b, MIN(3, 9) AS c"))

# %% Dates (SQLite keeps dates as text YYYY-MM-DD)
# strftime(format, date): write a date in a chosen format (%Y-%m = year-month).
print(q("SELECT order_id, order_date, strftime('%Y-%m', order_date) AS month FROM orders LIMIT 3"))
# Text dates in YYYY-MM-DD order compare correctly with >=.
print(q("SELECT order_id FROM orders WHERE order_date >= '2024-04-01'"))
# julianday(date): date as a day number, so subtracting gives days between.
print(q("SELECT julianday('2024-03-15') - julianday('2024-01-01') AS days"))

conn.close()
