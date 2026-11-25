class Paciente:
    """Paciente do sistema (Associação 1 para N com o SistemaAcolheMind)."""

    def __init__(self, nome: str, id_perfil: str, neuroatipicidade: str):
        self.nome = nome
        self.id_perfil = id_perfil
        self.neuroatipicidade = neuroatipicidade

    @property
    def condicao(self) -> str:
        """No banco de dados a coluna se chama 'condicao'."""
        return self.neuroatipicidade

    def exibir_perfil(self) -> str:
        return (
            f"Paciente: {self.nome} ({self.id_perfil}) "
            f"| Condição: {self.neuroatipicidade}"
        )
