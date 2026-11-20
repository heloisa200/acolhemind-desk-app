import pandas as pd

from repositories.paciente_repository import (
    PacienteRepository
)


class ExcelService:

    @staticmethod
    def exportar_pacientes():

        pacientes = (
            PacienteRepository.listar()
        )

        df = pd.DataFrame(
            pacientes,
            columns=[
                "ID",
                "Nome",
                "Condicao"
            ]
        )

        df.to_excel(
            "exports/pacientes.xlsx",
            index=False
        )

        return True