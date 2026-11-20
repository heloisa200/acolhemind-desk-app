from repositories.paciente_repository import (
    PacienteRepository
)

print("ANTES")

print(
    PacienteRepository.listar()
)

PacienteRepository.excluir(1)

print()

print("DEPOIS")

print(
    PacienteRepository.listar()
)