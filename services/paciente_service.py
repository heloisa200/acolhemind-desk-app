from repositories.paciente_repository import (
    PacienteRepository
)


class PacienteService:

    @staticmethod
    def atualizar(
        paciente_id,
        nome,
        condicao
    ):

        PacienteRepository.atualizar(
            paciente_id,
            nome,
            condicao
        )

        return True

    @staticmethod
    def excluir(
        paciente_id
    ):

        PacienteRepository.excluir(
            paciente_id
        )

        return True