import pandas as pd

from repositories.consulta_repository import (
    ConsultaRepository
)


class ExcelConsultasService:

    @staticmethod
    def exportar():

        consultas = (
            ConsultaRepository.listar()
        )

        df = pd.DataFrame(
            consultas,
            columns=[
                "ID",
                "Paciente_ID",
                "Motivo",
                "Sintoma",
                "Observacao",
                "Data"
            ]
        )

        df.to_excel(
            "exports/consultas.xlsx",
            index=False
        )

        return True