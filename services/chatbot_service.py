from repositories.consulta_repository import (
    ConsultaRepository
)


class ChatbotService:

    @staticmethod
    def responder(
        paciente_id,
        pergunta
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

        pergunta = pergunta.lower()

        if "ansiedade" in pergunta:

            if "ansiedade" in historico.lower():

                return (
                    "Ansiedade foi encontrada "
                    "no histórico clínico."
                )

            return (
                "Nenhum registro de ansiedade encontrado."
            )

        if "sintomas" in pergunta:

            return historico

        return (
            "Não encontrei resposta para essa pergunta."
        )