from reportlab.pdfgen import canvas


def gerar_pdf(texto, arquivo):

    pdf = canvas.Canvas(arquivo)

    y = 800

    for linha in texto.split("\n"):

        pdf.drawString(
            50,
            y,
            linha
        )

        y -= 20

    pdf.save()