from database.connection import conectar


class PacienteRepository:

    @staticmethod
    def salvar(
        nome,
        condicao
    ):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO pacientes
            (
                nome,
                condicao
            )
            VALUES
            (
                ?,
                ?
            )
            """,
            (
                nome,
                condicao
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
            SELECT
                id,
                nome,
                condicao
            FROM pacientes
            ORDER BY id DESC
            """
        )

        pacientes = cursor.fetchall()

        conn.close()

        return pacientes

    @staticmethod
    def atualizar(
        paciente_id,
        nome,
        condicao
    ):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE pacientes
            SET
                nome = ?,
                condicao = ?
            WHERE id = ?
            """,
            (
                nome,
                condicao,
                paciente_id
            )
        )

        conn.commit()

        conn.close()

    @staticmethod
    def excluir(
        paciente_id
    ):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM pacientes
            WHERE id = ?
            """,
            (
                paciente_id,
            )
        )

        conn.commit()

        conn.close()