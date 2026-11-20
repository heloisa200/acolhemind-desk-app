from database.connection import conectar


class ConsultaRepository:

    @staticmethod
    def salvar(
        paciente_id,
        motivo,
        sintoma,
        observacao
    ):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO consultas
            (
                paciente_id,
                motivo,
                sintoma,
                observacao
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?
            )
            """,
            (
                paciente_id,
                motivo,
                sintoma,
                observacao
            )
        )

        conn.commit()

        conn.close()

    @staticmethod
    def listar():

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM consultas
            ORDER BY id DESC
            """
        )

        consultas = cursor.fetchall()

        conn.close()

        return consultas

    @staticmethod
    def listar_por_paciente(
        paciente_id
    ):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                motivo,
                sintoma,
                observacao,
                data_consulta
            FROM consultas
            WHERE paciente_id = ?
            ORDER BY id DESC
            """,
            (
                paciente_id,
            )
        )

        consultas = cursor.fetchall()

        conn.close()

        return consultas