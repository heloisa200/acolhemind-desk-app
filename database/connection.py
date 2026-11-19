import sqlite3

def conectar():
    return sqlite3.connect(
        "database/acolhemind.db"
    )

def criar_banco():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            condicao TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()