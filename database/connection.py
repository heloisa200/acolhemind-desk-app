import sqlite3
from pathlib import Path

# Caminho absoluto: funciona não importa de qual pasta você rode o app
DB_PATH = Path(__file__).resolve().parent / "acolhemind.db"


def conectar():
    return sqlite3.connect(DB_PATH)


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

    # Tabela de usuários (administrador). A senha NUNCA é guardada em texto:
    # só o hash (PBKDF2) e o salt.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()
