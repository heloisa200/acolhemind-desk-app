import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/acolhemind.db"
)

df = pd.read_sql(
    """
    SELECT *
    FROM consultas
    """,
    conn
)

print(df)

conn.close()