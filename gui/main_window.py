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

        self.root = ctk.CTk()

        self.root.title("AcolheMind")

        self.root.geometry("1000x800")

        self.criar_tela()

    def criar_tela(self):

        titulo = ctk.CTkLabel(
            self.root,
            text="AcolheMind",
            font=("Arial", 24, "bold")
        )

        titulo.pack(pady=20)

        self.nome = ctk.CTkEntry(
            self.root,
            width=500,
            placeholder_text="Nome do paciente"
        )

        self.nome.pack(pady=10)

        self.condicao = ctk.CTkEntry(
            self.root,
            width=500,
            placeholder_text="Condição"
        )

        self.condicao.pack(pady=10)

        self.paciente_selecionado = ctk.CTkComboBox(
            self.root,
            values=["Selecione um paciente"]
        )

        self.paciente_selecionado.pack(pady=10)

        self.motivo = ctk.CTkEntry(
            self.root,
            width=600,
            placeholder_text="Motivo da consulta"
        )

        self.motivo.pack(pady=10)

        self.sintoma = ctk.CTkTextbox(
            self.root,
            width=700,
            height=120
        )

        self.sintoma.pack(pady=10)

        self.observacao = ctk.CTkTextbox(
            self.root,
            width=700,
            height=120
        )

        self.observacao.pack(pady=10)

        salvar_btn = ctk.CTkButton(
            self.root,
            text="Salvar Paciente",
            command=self.salvar_paciente
        )

        salvar_btn.pack(pady=5)

        consulta_btn = ctk.CTkButton(
            self.root,
            text="Registrar Consulta",
            command=self.salvar_consulta
        )

        consulta_btn.pack(pady=5)

        self.lista_pacientes = ctk.CTkTextbox(
            self.root,
            width=700,
            height=180
        )

        self.lista_pacientes.pack(pady=20)

        self.atualizar_lista()

    def atualizar_lista(self):

        self.lista_pacientes.delete(
            "0.0",
            "end"
        )

        pacientes = PacienteRepository.listar()

        nomes = []

        for paciente in pacientes:

            nomes.append(
                f"{paciente[0]} - {paciente[1]}"
            )

            self.lista_pacientes.insert(
                "end",
                f"{paciente[0]} - "
                f"{paciente[1]} - "
                f"{paciente[2]}\n"
            )

        if nomes:

            self.paciente_selecionado.configure(
                values=nomes
            )

    def salvar_paciente(self):

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

        self.atualizar_lista()

    def salvar_consulta(self):

        paciente = self.paciente_selecionado.get()

        if paciente == "Selecione um paciente":
            print("Selecione um paciente")
            return

        paciente_id = int(
            paciente.split("-")[0].strip()
        )

        motivo = self.motivo.get()

        sintoma = self.sintoma.get(
            "0.0",
            "end"
        )

        observacao = self.observacao.get(
            "0.0",
            "end"
        )

        ConsultaRepository.salvar(
            paciente_id,
            motivo,
            sintoma,
            observacao
        )

        gerar_relatorio_pdf(
            paciente,
            motivo,
            sintoma,
            observacao
        )

        print("CONSULTA GRAVADA")

    def executar(self):

        self.root.mainloop()