from repositories.consulta_repository import (
    ConsultaRepository
)

from services.ia_local_service import (
    IALocalService
)


class IAResumoService:

    @staticmethod
    def resumir_paciente(
        paciente_id
    ):

        consultas = (
            ConsultaRepository
            .listar_por_paciente(
                paciente_id
            )
        )

        historico = ""

        for consulta in consultas:

            historico += (
                f"Motivo: {consulta[0]}\n"
                f"Sintoma: {consulta[1]}\n"
                f"Observacao: {consulta[2]}\n\n"
            )

        prompt = f"""
Analise o histórico abaixo.

Identifique:
- sintomas recorrentes
- possíveis padrões
- evolução observada

Não realize diagnóstico.

Histórico:

{historico}
"""

        return (
            IALocalService
            .responder(
                prompt
            )
        )