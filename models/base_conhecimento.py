from typing import List


class BaseConhecimento:
    """Relação de Associação (Agregação) com o sistema."""

    def __init__(self, manuais: List[str]):
        self.manuais = manuais

    def consultar_diretrizes(self) -> str:
        return f"Validado via: {', '.join(self.manuais)}"
