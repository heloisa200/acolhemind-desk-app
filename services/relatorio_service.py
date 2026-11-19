from services.pdf_service import gerar_pdf


def gerar_relatorio_pdf(
    paciente,
    motivo,
    sintoma,
    observacao
):

    texto = f"""
ACOLHEMIND

Paciente:
{paciente}

Motivo:
{motivo}

Sintomas:
{sintoma}

Observações:
{observacao}
"""

    arquivo = (
        f"exports/{paciente}.pdf"
    )

    gerar_pdf(
        texto,
        arquivo
    )