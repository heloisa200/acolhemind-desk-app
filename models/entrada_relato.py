from abc import ABC, abstractmethod


class EntradaRelato(ABC):
    """Classe base abstrata (Herança e Polimorfismo)."""

    def __init__(self, conteudo: str):
        self.conteudo = conteudo

    @abstractmethod
    def extrair_sintomas(self) -> str:
        pass


class RelatoTexto(EntradaRelato):
    def extrair_sintomas(self) -> str:
        return f"[Texto]: {self.conteudo}"


class RelatoAudio(EntradaRelato):
    def __init__(self, conteudo: str, duracao_segundos: int):
        super().__init__(conteudo)
        self.duracao_segundos = duracao_segundos

    def extrair_sintomas(self) -> str:
        return f"[Áudio transcrito - {self.duracao_segundos}s]: {self.conteudo}"
