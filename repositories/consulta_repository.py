from database.connection import conectar


class ConsultaRepository:

    @staticmethod
    def salvar(paciente_id, motivo, sintoma, observacao):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO consultas (paciente_id, motivo, sintoma, observacao)
            VALUES (?, ?, ?, ?)
            """,
            (paciente_id, motivo, sintoma, observacao),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def listar():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consultas ORDER BY id DESC")
        consultas = cursor.fetchall()
        conn.close()
        return consultas

    @staticmethod
    def listar_completo():
        """Consultas já com o nome do paciente (usado na planilha Excel)."""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.id, c.paciente_id, p.nome, c.motivo, c.sintoma,
                   c.observacao, c.data_consulta
            FROM consultas c
            LEFT JOIN pacientes p ON p.id = c.paciente_id
            ORDER BY c.id DESC
            """
        )
        consultas = cursor.fetchall()
        conn.close()
        return consultas
