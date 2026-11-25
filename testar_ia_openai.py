from services.ia_service import (
    IAService
)

resposta = IAService.responder(
    "Explique ansiedade em uma frase."
)

print(
    resposta
)