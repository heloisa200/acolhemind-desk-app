from repositories.consulta_repository import (
    ConsultaRepository
)


class ConsultaService:

    @staticmethod
    def salvar(
        paciente_id,
        motivo,
        sintoma,
        observacao
    ):

        ConsultaRepository.salvar(
            paciente_id,
            motivo,
            sintoma,
            observacao
        )

        return True

    @staticmethod
    def listar_por_paciente(
        paciente_id
    ):

        return (
            ConsultaRepository
            .listar_por_paciente(
                paciente_id
            )
        )