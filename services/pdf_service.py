from reportlab.pdfgen import canvas

def gerar_pdf(
    texto,
    arquivo
):

    pdf = canvas.Canvas(
        arquivo
    )

    pdf.drawString(
        50,
        800,
        texto
    )

    pdf.save()