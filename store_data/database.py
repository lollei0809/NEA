import sqlite3
conn = sqlite3.connect("binary_app.sqlite")
cursor = conn.cursor()

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  password TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  age INTEGER,
);
"""

try:
    cursor.execute(create_users_table)

finally:
    conn.close()