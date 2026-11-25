from services.pdf_service import (
    gerar_pdf
)

from services.ia_resumo_service import (
    IAResumoService
)


def gerar_relatorio_pdf(
    paciente,
    paciente_id,
    motivo,
    sintoma,
    observacao
):

    resumo_ia = (
        IAResumoService.resumir_paciente(
            paciente_id
        )
    )

    texto = f"""
ACOLHEMIND

PACIENTE:
{paciente}

MOTIVO:
{motivo}

SINTOMAS:
{sintoma}

OBSERVACOES:
{observacao}

--------------------------------

RESUMO GERADO PELA IA

{resumo_ia}

--------------------------------
"""

    arquivo = (
        f"exports/{paciente}.pdf"
    )

    gerar_pdf(
        texto,
        arquivo
    )

    return arquivo