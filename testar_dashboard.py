from services.dashboard_service import (
    DashboardService
)

print(
    "Pacientes:",
    DashboardService.total_pacientes()
)

print(
    "Consultas:",
    DashboardService.total_consultas()
)

print(
    "PDFs:",
    DashboardService.total_pdfs()
)