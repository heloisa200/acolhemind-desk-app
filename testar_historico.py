from repositories.consulta_repository import (
    ConsultaRepository
)

consultas = (
    ConsultaRepository
    .listar_por_paciente(1)
)

print("CONSULTAS ENCONTRADAS:")

for consulta in consultas:

    print()

    print("Motivo:", consulta[0])

    print("Sintoma:", consulta[1])

    print("Observação:", consulta[2])

    print("Data:", consulta[3])