import customtkinter as ctk

from repositories.paciente_repository import (
    PacienteRepository
)

from repositories.consulta_repository import (
    ConsultaRepository
)

from services.relatorio_service import (
    gerar_relatorio_pdf
)


class MainWindow:

    def __init__(self):

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()

        self.root.title("AcolheMind")

        self.root.geometry("1200x900")

        self.criar_tela()

    def criar_tela(self):

        titulo = ctk.CTkLabel(
            self.root,
            text="AcolheMind",
            font=("Arial", 28, "bold")
        )

        titulo.pack(pady=20)

        # ==========================
        # Cadastro Paciente
        # ==========================

        self.nome = ctk.CTkEntry(
            self.root,
            width=500,
            placeholder_text="Nome do paciente"
        )

        self.nome.pack(pady=5)

        self.condicao = ctk.CTkEntry(
            self.root,
            width=500,
            placeholder_text="Condição"
        )

        self.condicao.pack(pady=5)

        salvar_btn = ctk.CTkButton(
            self.root,
            text="Salvar Paciente",
            command=self.salvar_paciente
        )

        salvar_btn.pack(pady=10)

        # ==========================
        # Seleção Paciente
        # ==========================

        self.paciente_selecionado = ctk.CTkComboBox(
            self.root,
            values=["Selecione um paciente"],
            width=500
        )

        self.paciente_selecionado.pack(pady=10)

        # ==========================
        # Consulta
        # ==========================

        self.motivo = ctk.CTkEntry(
            self.root,
            width=700,
            placeholder_text="Motivo da consulta"
        )

        self.motivo.pack(pady=5)

        lbl_sintoma = ctk.CTkLabel(
            self.root,
            text="Sintomas"
        )

        lbl_sintoma.pack()

        self.sintoma = ctk.CTkTextbox(
            self.root,
            width=700,
            height=120
        )

        self.sintoma.pack(pady=5)

        lbl_obs = ctk.CTkLabel(
            self.root,
            text="Observações"
        )

        lbl_obs.pack()

        self.observacao = ctk.CTkTextbox(
            self.root,
            width=700,
     