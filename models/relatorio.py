from typing import List

from models.paciente import Paciente


class RelatorioClinico:
    """Relação de Composição: nasce e morre dentro da sessão do sistema."""

    def __init__(self, motivo_consulta: str):
        self.motivo_consulta = motivo_consulta
        self.sintomas_principais: List[str] = []
        self.gatilhos_sobrecarga: List[str] = []

    def adicionar_dados(self, sintoma: str, gatilho: str):
        if sintoma:
            self.sintomas_principais.append(sintoma)
        if gatilho and gatilho not in self.gatilhos_sobrecarga:
            self.gatilhos_sobrecarga.append(gatilho)

    def gerar_texto_resumo(self, paciente: Paciente, validacao_rag: str) -> str:
        sintomas = (
            "\n  - ".join(self.sintomas_principais)
            if self.sintomas_principais
            else "Nenhum registrado"
        )
        gatilhos = (
            ", ".join(self.gatilhos_sobrecarga)
            if self.gatilhos_sobrecarga
            else "Nenhum informado"
        )

        return (
            "====================================================\n"
            "   RESUMO CLÍNICO OBJETIVO (LEITURA MÉDICA < 30s)   \n"
            "====================================================\n"
            f"• {paciente.exibir_perfil()}\n"
            f"• Motivo da Consulta: {self.motivo_consulta}\n\n"
            "• Sintomas Principais:\n"
            f"  - {sintomas}\n\n"
            f"• Gatilhos de Sobrecarga: {gatilhos}\n"
            "----------------------------------------------------\n"
            f"Status RAG: {validacao_rag}\n"
            "===================================================="
        )
