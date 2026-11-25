from typing import Dict, Iterable, Optional

from models.base_conhecimento import BaseConhecimento
from models.entrada_relato import EntradaRelato
from models.moderador_clinico import ModeradorClinico
from models.paciente import Paciente
from models.relatorio import RelatorioClinico


class SistemaAcolheMind:
    

    def __init__(self, base_dados: BaseConhecimento):
        self.base_conhecimento = base_dados
        self.pacientes_cadastrados: Dict[str, Paciente] = {}
        self.sessao_relatorio: Optional[RelatorioClinico] = None

    def cadastrar_paciente(self, nome: str, id_perfil: str, neuroatipicidade: str) -> Paciente:
        novo = Paciente(nome, id_perfil, neuroatipicidade)
        self.pacientes_cadastrados[id_perfil] = novo
        return novo

    def sincronizar_pacientes(self, registros: Iterable[tuple]) -> None:
        """Recarrega os pacientes a partir do banco: (id, nome, condicao)."""
        self.pacientes_cadastrados.clear()
        for id_, nome, condicao in registros:
            self.cadastrar_paciente(nome, str(id_), condicao)

    def iniciar_sessao_consulta(self, motivo_consulta: str) -> None:
        self.sessao_relatorio = RelatorioClinico(motivo_consulta)

    def processar_interacao(
        self, entrada: EntradaRelato, moderador: ModeradorClinico, gatilho: str
    ) -> bool:
        texto_processado = entrada.extrair_sintomas()
        if moderador.validar_seguranca(entrada.conteudo) and self.sessao_relatorio:
            self.sessao_relatorio.adicionar_dados(texto_processado, gatilho)
            return True
        return False

    def gerar_resumo(self, id_perfil: str) -> str:
        paciente = self.pacientes_cadastrados[id_perfil]
        return self.sessao_relatorio.gerar_texto_resumo(
            paciente, self.base_conhecimento.consultar_diretrizes()
        )
