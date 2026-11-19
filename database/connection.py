import sqlite3


def conectar():
    return sqlite3.connect(
        "database/acolhemind.db"
    )


def criar_banco():

    conn = conectar()

    cursor = conn.cursor()

    # Tabela de pacientes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            condicao TEXT NOT NULL
        )
        """
    )

    # Tabela de consultas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            motivo TEXT,
            sintoma TEXT,
            observacao TEXT,
            data_consulta DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()