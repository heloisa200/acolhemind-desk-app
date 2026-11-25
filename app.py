import customtkinter as ctk

from database.connection import criar_banco
from gui.home_window import HomeWindow
from gui.login_window import LoginWindow
from gui.main_window import MainWindow
from gui.paciente_window import PacienteWindow

criar_banco()

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Loop: menu inicial -> (paciente | login -> painel do administrador) -> menu
# Fechar o menu inicial encerra o aplicativo.
while True:
    escolha = HomeWindow().executar()

    if escolha is None:
        break

    if escolha == "paciente":
        PacienteWindow().executar()

    elif escolha == "admin":
        usuario = LoginWindow().executar()
        if usuario is None:  # desistiu do login: volta ao menu
            continue
        MainWindow(usuario).executar()
