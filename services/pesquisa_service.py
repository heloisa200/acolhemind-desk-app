from repositories.paciente_repository import (
    PacienteRepository
)


class PesquisaService:

    @staticmethod
    def buscar(
        texto
    ):

        pacientes = (
            PacienteRepository.listar()
        )

        resultado = []

        for paciente in pacientes:

            nome = paciente[1]

            if texto.lower() in nome.lower():

                resultado.append(
                    paciente
                )

        return resultado