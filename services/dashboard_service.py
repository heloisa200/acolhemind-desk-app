from database.connection import conectar


class DashboardService:

    @staticmethod
    def total_pacientes():

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM pacientes
            """
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    @staticmethod
    def total_consultas():

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM consultas
            """
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    @staticmethod
    def resumo():

        return {
            "pacientes": DashboardService.total_pacientes(),
            "consultas": DashboardService.total_consultas()
        }