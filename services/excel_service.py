from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from repositories.consulta_repository import ConsultaRepository
from repositories.paciente_repository import PacienteRepository


def _seguro(valor):
    """Evita 'injeção de fórmula': texto que começa com = + - @ vira texto puro."""
    if isinstance(valor, str) and valor[:1] in ("=", "+", "-", "@"):
        return "'" + valor
    return valor


def _montar_aba(aba, cabecalho, linhas):
    aba.append(cabecalho)
    for celula in aba[1]:
        celula.font = Font(bold=True, color="FFFFFF")
        celula.fill = PatternFill("solid", fgColor="2B5B84")
        celula.alignment = Alignment(horizontal="center")

    for linha in linhas:
        aba.append([_seguro(v) for v in linha])

    # Largura das colunas conforme o conteúdo
    for i, coluna in enumerate(aba.columns, start=1):
        maior = max(len(str(c.value)) if c.value is not None else 0 for c in coluna)
        aba.column_dimensions[get_column_letter(i)].width = min(maior + 4, 60)

    aba.freeze_panes = "A2"


def exportar_excel(caminho: str) -> None:
    """Gera a planilha completa: pacientes + consultas."""
    wb = Workbook()

    aba_pac = wb.active
    aba_pac.title = "Pacientes"
    _montar_aba(
        aba_pac,
        ["ID", "Nome", "Condição"],
        PacienteRepository.listar(),
    )

    aba_con = wb.create_sheet("Consultas")
    _montar_aba(
        aba_con,
        ["ID", "ID Paciente", "Paciente", "Motivo", "Sintoma", "Observação", "Data"],
        ConsultaRepository.listar_completo(),
    )

    aba_info = wb.create_sheet("Informações")
    aba_info.append(["Gerado em", datetime.now().strftime("%d/%m/%Y %H:%M")])
    aba_info.append(["Aviso", "Documento confidencial: contém dados sensíveis de saúde."])
    aba_info.column_dimensions["A"].width = 14
    aba_info.column_dimensions["B"].width = 70

    wb.save(caminho)
