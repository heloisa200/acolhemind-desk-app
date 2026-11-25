class ModeradorClinico:
    """Relação de Dependência no processamento."""

    def validar_seguranca(self, texto: str) -> bool:
        return len(texto.strip()) > 2
