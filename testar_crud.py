from repositories.paciente_repository import (
    PacienteRepository
)

print("ANTES")

print(
    PacienteRepository.listar()
)

PacienteRepository.atualizar(
    1,
    "Heloisa Atualizada",
    "TEA"
)

print("DEPOIS DA ATUALIZACAO")

print(
    PacienteRepository.listar()
)