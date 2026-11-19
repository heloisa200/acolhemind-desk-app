def gerar_resumo(
    paciente,
    motivo,
    sintoma,
    observacao
):

    return f"""
PACIENTE: {paciente}

MOTIVO:
{motivo}

SINTOMAS:
{sintoma}

OBSERVAÇÕES:
{observacao}
"""