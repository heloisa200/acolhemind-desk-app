from database.connection import conectar

class PacienteRepository:

    def salvar(
        self,
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