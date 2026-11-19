import customtkinter as ctk

from repositories.paciente_repository import (
    PacienteRepository
)


class MainWindow:

    def __init__(self):

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()

        self.root.title(
            "AcolheMind"
        )

        self.root.geometry(
            "1000x700"
        )

        self.criar_tela()

    def criar_tela(self):

        titulo = ctk.CTkLabel(
            self.root,
            text="AcolheMind - Assistente Pré-Consulta",
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            pady=20
        )

        self.nome = ctk.CTkEntry(
            self.root,
            width=500,
            placeholder_text="Nome do paciente"
        )

        self.nome.pack(
            pady=10
        )

        self.condicao = ctk.CTkEntry(
            self.root,
            width=500,
            placeholder_text="Condição"
        )

        self.condicao.pack(
            pady=10
        )

        self.sintoma = ctk.CTkTextbox(
            self.root,
            width=700,
            height=150
        )

        self.sintoma.pack(
            pady=20
        )

        salvar = ctk.CTkButton(
            self.root,
            text="Salvar Paciente",
            command=self.salvar
        )

        salvar.pack(
            pady=10
        )

    def salvar(self):

        nome = self.nome.get()

        condicao = self.condicao.get()

        if not nome or not condicao:
            return

        PacienteRepository.salvar(
            nome,
            condicao
        )

        self.nome.delete(
            0,
            "end"
        )

        self.condicao.delete(
            0,
            "end"
        )

    def executar(self):

        self.root.mainloop()