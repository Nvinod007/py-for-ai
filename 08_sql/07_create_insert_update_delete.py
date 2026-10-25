# Changing data: CREATE TABLE, INSERT, UPDATE, DELETE, constraints, transactions.
# This file uses a scratch database so your shop.db stays untouched.
# Each line has a short comment saying WHAT it is.

import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
# sqlite3.connect(file): opens (or creates) the database file; conn is our open connection.
conn = sqlite3.connect(DATA / "output" / "scratch.db")
# PRAGMA foreign_keys = ON: make SQLite enforce links between tables (off by default).
conn.execute("PRAGMA foreign_keys = ON")


# q = small helper: runs SQL text and returns the result as a pandas table.
def q(sql, params=()):
    # read_sql_query(sql, conn, params=...): runs the SQL on the connection; params fill the ? marks safely.
    return pd.read_sql_query(sql, conn, params=params)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% CREATE TABLE with types and rules
# executescript: run several SQL statements at once.
# DROP TABLE IF EXISTS: delete a table if present. CREATE TABLE: make a table; each line is a column name + type.
# INTEGER/TEXT: whole number/text. PRIMARY KEY: unique id; AUTOINCREMENT: counts up by itself. NOT NULL: must have a value.
# UNIQUE: no repeats. REFERENCES projects(id): must match an existing project. DEFAULT: value used if none given.
# CHECK (...): rejects values that break the rule. CURRENT_TIMESTAMP: the time now.
conn.executescript("""
    DROP TABLE IF EXISTS tasks;
    DROP TABLE IF EXISTS projects;

    CREATE TABLE projects (
        id    INTEGER PRIMARY KEY,
        name  TEXT NOT NULL UNIQUE
    );

    CREATE TABLE tasks (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id  INTEGER NOT NULL REFERENCES projects(id),
        title       TEXT NOT NULL,
        priority    INTEGER DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
        done        INTEGER DEFAULT 0,
        created_at  TEXT DEFAULT CURRENT_TIMESTAMP
    );
""")

# %% INSERT
# INSERT INTO table (columns) VALUES (values): add a new row.
conn.execute("INSERT INTO projects (id, name) VALUES (1, 'Learn SQL')")
# ? placeholders get their values from the tuple (2, "Build RAG").
conn.execute("INSERT INTO projects (id, name) VALUES (?, ?)", (2, "Build RAG"))
# executemany(sql, list): run the same statement once for each tuple in the list.
conn.executemany(
    "INSERT INTO tasks (project_id, title, priority) VALUES (?, ?, ?)",
    [(1, "SELECT basics", 1), (1, "Joins", 2), (2, "Chunk documents", 3), (2, "Add evals", 2)],
)
# commit(): save the changes permanently.
conn.commit()
print(q("SELECT * FROM tasks"))

# %% UPDATE (always use WHERE!)
# UPDATE table SET col = value WHERE ...: change existing rows; no WHERE changes EVERY row.
cur = conn.execute("UPDATE tasks SET done = 1 WHERE title = ?", ("SELECT basics",))
# cur.rowcount: how many rows the last statement changed.
print("rows changed:", cur.rowcount)
# SET priority = priority + 1: new value can use the old one.
conn.execute("UPDATE tasks SET priority = priority + 1 WHERE project_id = 2")
conn.commit()
print(q("SELECT id, title, priority, done FROM tasks"))

# %% DELETE (always use WHERE!)
# DELETE FROM table WHERE ...: remove matching rows; no WHERE deletes everything.
conn.execute("DELETE FROM tasks WHERE done = 1")
conn.commit()
print(q("SELECT COUNT(*) AS left_over FROM tasks"))

# %% Transactions: all or nothing
try:
    # with conn: a transaction; if anything fails inside, ALL its changes are undone.
    with conn:                                          # commits, or rolls back on error
        conn.execute("INSERT INTO projects (id, name) VALUES (10, 'Temp')")
        conn.execute("INSERT INTO projects (id, name) VALUES (10, 'Duplicate id')")   # fails
except sqlite3.IntegrityError:
    print("rolled back")
print(q("SELECT * FROM projects"))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Rules protect your data
# Each statement breaks one rule; we loop and try them all.
for sql in [
    "INSERT INTO projects (id, name) VALUES (3, 'Learn SQL')",                 # UNIQUE
    "INSERT INTO tasks (project_id, title) VALUES (99, 'orphan')",             # FOREIGN KEY
    "INSERT INTO tasks (project_id, title, priority) VALUES (1, 'x', 9)",      # CHECK
    "INSERT INTO tasks (project_id) VALUES (1)",                               # NOT NULL
]:
    try:
        conn.execute(sql)
    # IntegrityError: the error SQLite raises when a rule (UNIQUE, CHECK, etc.) is broken.
    except sqlite3.IntegrityError as error:
        print("blocked:", error)

# %% Change a table
# ALTER TABLE ... ADD COLUMN: add a new column to an existing table.
conn.execute("ALTER TABLE tasks ADD COLUMN notes TEXT")
# CREATE INDEX name ON table(col): builds a lookup shortcut so searches on col are faster.
conn.execute("CREATE INDEX idx_tasks_project ON tasks(project_id)")      # faster lookups
print(q("PRAGMA table_info(tasks)")[["name", "type", "notnull"]])

# %% Upsert: insert or update if it exists
# ON CONFLICT(id) DO UPDATE SET ...: if that id already exists, update the row instead of failing; excluded.name = the new value we tried to insert.
conn.execute("""
    INSERT INTO projects (id, name) VALUES (1, 'Learn SQL v2')
    ON CONFLICT(id) DO UPDATE SET name = excluded.name
""")
print(q("SELECT * FROM projects WHERE id = 1"))

# %% Views: saved queries
# DROP VIEW IF EXISTS: delete a saved query if present.
conn.execute("DROP VIEW IF EXISTS open_tasks")
# CREATE VIEW name AS SELECT ...: save a query so you can use it like a table.
conn.execute("CREATE VIEW open_tasks AS SELECT title, priority FROM tasks WHERE done = 0")
print(q("SELECT * FROM open_tasks"))

conn.commit()
conn.close()
