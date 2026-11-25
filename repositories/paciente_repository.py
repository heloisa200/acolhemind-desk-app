from database.connection import conectar


class PacienteRepository:
    """CRUD de pacientes (Create, Read, Update, Delete)."""

    # CREATE (devolve o id do registro criado)
    @staticmethod
    def salvar(nome, condicao):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pacientes (nome, condicao) VALUES (?, ?)",
            (nome, condicao),
        )
        novo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return novo_id

    # READ (todos, com busca opcional por nome ou condição)
    @staticmethod
    def listar(busca=""):
        conn = conectar()
        cursor = conn.cursor()
        termo = f"%{busca}%"
        cursor.execute(
            """
            SELECT id, nome, condicao
            FROM pacientes
            WHERE nome LIKE ? OR condicao LIKE ?
            ORDER BY id DESC
            """,
            (termo, termo),
        )
        pacientes = cursor.fetchall()
        conn.close()
        return pacientes

    # READ (somente os ids informados: usado na área do paciente)
    @staticmethod
    def listar_por_ids(ids):
        ids = list(ids)
        if not ids:
            return []

        marcadores = ",".join("?" * len(ids))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT id, nome, condicao
            FROM pacientes
            WHERE id IN ({marcadores})
            ORDER BY id DESC
            """,
            ids,
        )
        pacientes = cursor.fetchall()
        conn.close()
        return pacientes

    # UPDATE
    @staticmethod
    def atualizar(paciente_id, nome, condicao):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pacientes SET nome = ?, condicao = ? WHERE id = ?",
            (nome, condicao, paciente_id),
        )
        conn.commit()
        conn.close()

    # DELETE
    @staticmethod
    def excluir(paciente_id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
        conn.commit()
        conn.close()
