from services.pdf_service import gerar_pdf

texto = """
AcolheMind

Paciente: Maria

Condição: TEA

Sintomas:
- Ansiedade
- Sensibilidade sensorial
"""

gerar_pdf(
    texto,
    "exports/teste.pdf"
)

print("PDF criado com sucesso!")
