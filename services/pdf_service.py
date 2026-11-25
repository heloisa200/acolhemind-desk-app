import textwrap

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def gerar_pdf(texto, arquivo):
    """Gera um PDF com o texto (várias linhas, quebra automática e páginas)."""
    pdf = canvas.Canvas(arquivo, pagesize=A4)
    largura, altura = A4

    fonte, tamanho = "Courier", 10
    margem, entrelinha = 50, 14
    max_chars = int((largura - 2 * margem) / pdf.stringWidth("M", fonte, tamanho))

    def nova_pagina():
        pdf.setFont(fonte, tamanho)
        return altura - margem

    y = nova_pagina()

    for linha in texto.splitlines():
        for trecho in textwrap.wrap(linha, max_chars, replace_whitespace=False) or [""]:
            if y < margem:
                pdf.showPage()
                y = nova_pagina()
            pdf.drawString(margem, y, trecho)
            y -= entrelinha

    pdf.save()
