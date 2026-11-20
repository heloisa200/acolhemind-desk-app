from services.pesquisa_service import (
    PesquisaService
)

resultado = (
    PesquisaService.buscar(
        "jo"
    )
)

print(resultado)