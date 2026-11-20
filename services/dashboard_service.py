import os

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
    def total_pdfs():

        pasta = "exports"

        if not os.path.exists(
            pasta
        ):
            return 0

        total = 0

        for arquivo in os.listdir(
            pasta
        ):

            if arquivo.lower().endswith(
                ".pdf"
            ):
                total += 1

        return total

    @staticmethod
    def resumo():

        return {
            "pacientes":
                DashboardService.total_pacientes(),

            "consultas":
                DashboardService.total_consultas(),

            "pdfs":
                DashboardService.total_pdfs()
        }