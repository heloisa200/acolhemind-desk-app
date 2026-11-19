from database.connection import conectar


class ConsultaRepository:

    @staticmethod
    def salvar(
        paciente_id,
        motivo,
        sintoma,
        observacao
    ):

        print("ENTROU NO REPOSITORY")

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
