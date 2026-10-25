# Changing data: CREATE TABLE, INSERT, UPDATE, DELETE, constraints, transactions.
# This file uses a scratch database so your shop.db stays untouched.

import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
conn = sqlite3.connect(DATA / "output" / "scratch.db")
conn.execute("PRAGMA foreign_keys = ON")


def q(sql, params=()):
    return pd.read_sql_query(sql, conn, params=params)


# %% CREATE TABLE with types and rules
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
conn.execute("INSERT INTO projects (id, name) VALUES (1, 'Learn SQL')")
conn.execute("INSERT INTO projects (id, name) VALUES (?, ?)", (2, "Build RAG"))
conn.executemany(
    "INSERT INTO tasks (project_id, title, priority) VALUES (?, ?, ?)",
    [(1, "SELECT basics", 1), (1, "Joins", 2), (2, "Chunk documents", 3), (2, "Add evals", 2)],
)
conn.commit()
print(q("SELECT * FROM tasks"))

# %% UPDATE (always use WHERE!)
cur = conn.execute("UPDATE tasks SET done = 1 WHERE title = ?", ("SELECT basics",))
print("rows changed:", cur.rowcount)
conn.execute("UPDATE tasks SET priority = priority + 1 WHERE project_id = 2")
conn.commit()
print(q("SELECT id, title, priority, done FROM tasks"))

# %% DELETE (always use WHERE!)
conn.execute("DELETE FROM tasks WHERE done = 1")
conn.commit()
print(q("SELECT COUNT(*) AS left_over FROM tasks"))

# %% Rules protect your data
for sql in [
    "INSERT INTO projects (id, name) VALUES (3, 'Learn SQL')",                 # UNIQUE
    "INSERT INTO tasks (project_id, title) VALUES (99, 'orphan')",             # FOREIGN KEY
    "INSERT INTO tasks (project_id, title, priority) VALUES (1, 'x', 9)",      # CHECK
    "INSERT INTO tasks (project_id) VALUES (1)",                               # NOT NULL
]:
    try:
        conn.execute(sql)
    except sqlite3.IntegrityError as error:
        print("blocked:", error)

# %% Transactions: all or nothing
try:
    with conn:                                          # commits, or rolls back on error
        conn.execute("INSERT INTO projects (id, name) VALUES (10, 'Temp')")
        conn.execute("INSERT INTO projects (id, name) VALUES (10, 'Duplicate id')")   # fails
except sqlite3.IntegrityError:
    print("rolled back")
print(q("SELECT * FROM projects"))

# %% Change a table
conn.execute("ALTER TABLE tasks ADD COLUMN notes TEXT")
conn.execute("CREATE INDEX idx_tasks_project ON tasks(project_id)")      # faster lookups
print(q("PRAGMA table_info(tasks)")[["name", "type", "notnull"]])

# %% Upsert: insert or update if it exists
conn.execute("""
    INSERT INTO projects (id, name) VALUES (1, 'Learn SQL v2')
    ON CONFLICT(id) DO UPDATE SET name = excluded.name
""")
print(q("SELECT * FROM projects WHERE id = 1"))

# %% Views: saved queries
conn.execute("DROP VIEW IF EXISTS open_tasks")
conn.execute("CREATE VIEW open_tasks AS SELECT title, priority FROM tasks WHERE done = 0")
print(q("SELECT * FROM open_tasks"))

conn.commit()
conn.close()
