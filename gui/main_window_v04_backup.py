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
            height=120
        )

        self.observacao.pack(pady=5)

        consulta_btn = ctk.CTkButton(
            self.root,
            text="Registrar Consulta",
            command=self.salvar_consulta
        )

        consulta_btn.pack(pady=10)

        historico_btn = ctk.CTkButton(
            self.root,
            text="Ver Histórico",
            command=self.carregar_historico
        )

        historico_btn.pack(pady=5)

        # ==========================
        # Lista de Pacientes
        # ==========================

        lbl_lista = ctk.CTkLabel(
            self.root,
            text="Pacientes cadastrados"
        )

        lbl_lista.pack()

        self.lista_pacientes = ctk.CTkTextbox(
            self.root,
            width=900,
            height=150
        )

        self.lista_pacientes.pack(
            pady=10
        )

        # ==========================
        # Histórico
        # ==========================

        lbl_hist = ctk.CTkLabel(
            self.root,
            text="Histórico de Consultas"
        )

        lbl_hist.pack()

        self.historico = ctk.CTkTextbox(
            self.root,
            width=900,
            height=250
        )

        self.historico.pack(
            pady=10
        )

        self.atualizar_lista()

    # ====================================
    # Pacientes
    # ====================================

    def atualizar_lista(self):

        self.lista_pacientes.delete(
            "0.0",
            "end"
        )

        pacientes = (
            PacienteRepository.listar()
        )

        nomes = []

        for paciente in pacientes:

            nomes.append(
                f"{paciente[0]} - {paciente[1]}"
            )

            self.lista_pacientes.insert(
                "end",
                f"ID: {paciente[0]} | "
                f"Nome: {paciente[1]} | "
                f"Condição: {paciente[2]}\n"
            )

        if nomes:

            self.paciente_selecionado.configure(
                values=nomes
            )

    def salvar_paciente(self):

        nome = self.nome.get()

        condicao = self.condicao.get()

        if not nome:
            return

        if not condicao:
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

    # ====================================
    # Consultas
    # ====================================

    def salvar_consulta(self):

        paciente = (
            self.paciente_selecionado.get()
        )

        if paciente == "Selecione um paciente":
            return

        paciente_id = int(
            paciente.split("-")[0].strip()
        )

        motivo = self.motivo.get()

        sintoma = self.sintoma.get(
            "0.0",
            "end"
        ).strip()

        observacao = self.observacao.get(
            "0.0",
            "end"
        ).strip()

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

        print(
            "CONSULTA GRAVADA"
        )

        self.carregar_historico()

    # ====================================
    # Histórico
    # ====================================

    def carregar_historico(self):

        paciente = (
            self.paciente_selecionado.get()
        )

        if paciente == "Selecione um paciente":
            return

        paciente_id = int(
            paciente.split("-")[0].strip()
        )

        consultas = (
            ConsultaRepository
            .listar_por_paciente(
                paciente_id
            )
        )

        self.historico.delete(
            "0.0",
            "end"
        )

        if len(consultas) == 0:

            self.historico.insert(
                "0.0",
                "Nenhuma consulta encontrada."
            )

            return

        texto = ""

        for consulta in consultas:

            texto += (
                f"Data: {consulta[3]}\n"
                f"Motivo: {consulta[0]}\n"
                f"Sintoma: {consulta[1]}\n"
                f"Observação: {consulta[2]}\n"
                "\n"
                "----------------------------------------\n\n"
            )

        self.historico.insert(
            "0.0",
            texto
        )

    def executar(self):

        self.root.mainloop()