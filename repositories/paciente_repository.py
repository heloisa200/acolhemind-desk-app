from database.connection import conectar

class PacienteRepository:

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
            """
        )

        dados = cursor.fetchall()

        conn.close()

        return dados