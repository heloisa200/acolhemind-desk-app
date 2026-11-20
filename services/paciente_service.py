from repositories.paciente_repository import (
    PacienteRepository
)


class PacienteService:

    @staticmethod
    def salvar(
        nome,
        condicao
    ):

        if not nome:
            return False

        if not condicao:
            return False

        PacienteRepository.salvar(
            nome,
            condicao
        )

        return True

    @staticmethod
    def listar():

        return (
            PacienteRepository
            .listar()
        )