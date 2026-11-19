import sqlite3

conn = sqlite3.connect(
    "database/acolhemind.db"
)

cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master"
)

for item in cursor.fetchall():
    print(item)

conn.close()