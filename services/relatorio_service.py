from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from repositories.consulta_repository import ConsultaRepository
from repositories.paciente_repository import PacienteRepository

COR_CABECALHO = colors.HexColor("#2B5B84")
COR_LINHA_ALTERNADA = colors.HexColor("#F2F6FA")


def _texto(valor):
    """Escapa o texto para o Paragraph não interpretar '<', '&' como marcação."""
    if valor is None:
        return ""
    return escape(str(valor)).replace("\n", "<br/>")


def _tabela(cabecalho, linhas, larguras_cm, estilo_celula, estilo_cabecalho):
    dados = [[Paragraph(_texto(c), estilo_cabecalho) for c in cabecalho]]
    for linha in linhas:
        dados.append([Paragraph(_texto(c), estilo_celula) for c in linha])

    tabela = Table(dados, colWidths=[l * cm for l in larguras_cm], repeatRows=1)
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), COR_CABECALHO),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COR_LINHA_ALTERNADA]),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B8C4CF")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return tabela


def _rodape(canvas, doc):
    largura, _ = landscape(A4)
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5D6D7E"))
    canvas.drawString(
        1.5 * cm, 1 * cm, "Documento confidencial - contém dados sensíveis de saúde."
    )
    canvas.drawRightString(largura - 1.5 * cm, 1 * cm, f"Página {doc.page}")
    canvas.restoreState()


def gerar_relatorio_pdf(caminho, administrador=""):
    """Relatório geral do administrador: pacientes e consultas."""
    pacientes = sorted(PacienteRepository.listar(), key=lambda p: p[0])
    consultas = sorted(ConsultaRepository.listar_completo(), key=lambda c: c[0])

    estilos = getSampleStyleSheet()
    celula = ParagraphStyle("celula", parent=estilos["BodyText"], fontSize=8.5, leading=11)
    cabecalho = ParagraphStyle(
        "cabecalho", parent=celula, textColor=colors.white, fontName="Helvetica-Bold"
    )

    quem = f" por {_texto(administrador)}" if administrador else ""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    elementos = [
        Paragraph("AcolheMind - Relatório Geral", estilos["Title"]),
        Paragraph(f"Gerado em {agora}{quem}", estilos["BodyText"]),
        Spacer(1, 0.3 * cm),
        Paragraph(
            f"<b>Total de pacientes:</b> {len(pacientes)} &nbsp;&nbsp; "
            f"<b>Total de consultas:</b> {len(consultas)}",
            estilos["BodyText"],
        ),
        Spacer(1, 0.4 * cm),
        Paragraph("Pacientes", estilos["Heading2"]),
    ]

    if pacientes:
        elementos.append(
            _tabela(["ID", "Nome", "Condição"], pacientes, [1.5, 9, 16.2], celula, cabecalho)
        )
    else:
        elementos.append(Paragraph("Nenhum paciente cadastrado.", estilos["BodyText"]))

    elementos += [Spacer(1, 0.6 * cm), Paragraph("Consultas", estilos["Heading2"])]

    if consultas:
        elementos.append(
            _tabela(
                ["ID", "Paciente", "Motivo", "Sintoma", "Observação", "Data"],
                [(c[0], c[2] or f"(paciente {c[1]} removido)", c[3], c[4], c[5], c[6]) for c in consultas],
                [1.2, 4.0, 4.5, 6.0, 7.5, 3.5],
                celula,
                cabecalho,
            )
        )
    else:
        elementos.append(Paragraph("Nenhuma consulta registrada.", estilos["BodyText"]))

    doc = SimpleDocTemplate(
        caminho,
        pagesize=landscape(A4),
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.8 * cm,
        title="Relatório Geral - AcolheMind",
    )
    doc.build(elementos, onFirstPage=_rodape, onLaterPages=_rodape)
