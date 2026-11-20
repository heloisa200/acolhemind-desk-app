from repositories.paciente_repository import (
    PacienteRepository
)

pacientes = (
    PacienteRepository.listar()
)

for paciente in pacientes:

    print(
        f"ID: {paciente[0]}"
    )

    print(
        f"Nome: {paciente[1]}"
    )

    print(
        f"Condição: {paciente[2]}"
    )

    print()