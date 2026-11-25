from datetime import datetime
from queue import Empty, Queue
from threading import Thread
from tkinter import ttk, messagebox, filedialog

import customtkinter as ctk

from app_acolhemind import SistemaAcolheMind
from models.base_conhecimento import BaseConhecimento
from models.consulta import ConsultaFrame
from models.moderador_clinico import ModeradorClinico
from repositories.paciente_repository import PacienteRepository
from services.audio_service import AudioServiceError
from services.excel_service import exportar_excel

MODO_TEXTO = "Texto"
MODO_AUDIO = "Áudio (português)"
MAX_DURACAO_AUDIO = 300

# Cores da tabela (Treeview) para cada tema
CORES_TABELA = {
    "Light": {
        "bg": "#FFFFFF", "fg": "#1A1A1A",
        "cab_bg": "#E5E5E5", "cab_fg": "#1A1A1A",
        "sel": "#3B8ED0",
    },
    "Dark": {
        "bg": "#2B2B2B", "fg": "#DCE4EE",
        "cab_bg": "#1F1F1F", "cab_fg": "#DCE4EE",
        "sel": "#1F6AA5",
    },
}


class MainWindow:

    def __init__(self, usuario="admin"):
        self.usuario = usuario
        self.voltar_ao_login = False  # True quando o admin clica em Sair

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("AcolheMind - Painel do Administrador")
        self.root.geometry("1000x700")

        self.paciente_selecionado = None  # id do paciente em edição (None = novo)
        self.janela_consultas = None
        self.consulta_frame = None
        self._fila_audio_condicao = Queue()
        self._gravacao_condicao_em_andamento = False

        self.criar_tela()
        self.aplicar_estilo_tabela()
        self.atualizar_lista()
        self.root.after(100, self._processar_fila_audio_condicao)

    # ------------------------------------------------------------------
    # INTERFACE
    # ------------------------------------------------------------------
    def criar_tela(self):
        # ----- Cabeçalho: título + botão de tema -----
        topo = ctk.CTkFrame(self.root, fg_color="transparent")
        topo.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            topo,
            text="AcolheMind - Cadastro de Pacientes",
            font=("Arial", 24, "bold"),
        ).pack(side="left")

        self.switch_tema = ctk.CTkSwitch(
            topo,
            text="Modo escuro",
            command=self.alternar_tema,
        )
        self.switch_tema.pack(side="right")

        # ----- Barra do administrador -----
        barra = ctk.CTkFrame(self.root, fg_color="transparent")
        barra.pack(fill="x", padx=20)

        ctk.CTkLabel(
            barra, text=f"Administrador: {self.usuario}", text_color="gray50"
        ).pack(side="left")

        ctk.CTkButton(
            barra, text="Sair", width=90,
            fg_color="gray50", hover_color="gray35",
            command=self.sair,
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            barra, text="Exportar Excel", width=140,
            fg_color="#1D7A46", hover_color="#155B34",
            command=self.exportar,
        ).pack(side="right")

        ctk.CTkButton(
            barra, text="Consultas", width=120,
            command=self.abrir_consultas,
        ).pack(side="right", padx=(0, 10))

        # ----- Formulário -----
        form = ctk.CTkFrame(self.root)
        form.pack(fill="x", padx=20, pady=10)

        self.lbl_modo = ctk.CTkLabel(
            form, text="Novo paciente", font=("Arial", 14, "bold")
        )
        self.lbl_modo.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 0))

        self.nome = ctk.CTkEntry(form, width=360, placeholder_text="Nome do paciente")
        self.nome.grid(row=1, column=0, padx=15, pady=10)

        self.condicao = ctk.CTkEntry(form, width=360, placeholder_text="Condição")
        self.condicao.grid(row=1, column=1, padx=15, pady=10)

        self.entrada_condicao = ctk.CTkFrame(form, fg_color="transparent")
        self.entrada_condicao.grid(
            row=2, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 8)
        )
        ctk.CTkLabel(self.entrada_condicao, text="Relatar por:").pack(side="left")
        self.modo_condicao = ctk.CTkOptionMenu(
            self.entrada_condicao,
            values=[MODO_TEXTO, MODO_AUDIO],
            command=self._ao_trocar_modo_condicao,
            width=170,
        )
        self.modo_condicao.pack(side="left", padx=(8, 0))
        self.duracao_condicao = ctk.CTkEntry(
            self.entrada_condicao,
            width=110,
            placeholder_text="Segundos",
        )
        self.duracao_condicao.insert(0, "5")
        self.btn_audio_condicao = ctk.CTkButton(
            self.entrada_condicao,
            text="Gravar áudio",
            width=120,
            command=self.gravar_audio_condicao,
        )
        self.status_audio_condicao = ctk.CTkLabel(
            self.entrada_condicao, text="", text_color="gray50"
        )

        botoes = ctk.CTkFrame(form, fg_color="transparent")
        botoes.grid(row=3, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 12))

        self.btn_salvar = ctk.CTkButton(
            botoes, text="Salvar", width=120, command=self.salvar
        )
        self.btn_salvar.pack(side="left", padx=(0, 10))

        self.btn_excluir = ctk.CTkButton(
            botoes, text="Excluir", width=120,
            fg_color="#C0392B", hover_color="#962D22",
            command=self.excluir, state="disabled",
        )
        self.btn_excluir.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            botoes, text="Limpar", width=120,
            fg_color="gray50", hover_color="gray35",
            command=self.limpar_formulario,
        ).pack(side="left")

        # ----- Busca -----
        self.busca = ctk.CTkEntry(
            self.root, width=400, placeholder_text="Buscar por nome ou condição..."
        )
        self.busca.pack(anchor="w", padx=20, pady=(5, 5))
        self.busca.bind("<KeyRelease>", lambda e: self.atualizar_lista())

        # ----- Tabela -----
        area_tabela = ctk.CTkFrame(self.root)
        area_tabela.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tabela = ttk.Treeview(
            area_tabela,
            columns=("id", "nome", "condicao"),
            show="headings",
            selectmode="browse",
            style="Acolhe.Treeview",
        )
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("condicao", text="Condição")
        self.tabela.column("id", width=60, anchor="center", stretch=False)
        self.tabela.column("nome", width=350)
        self.tabela.column("condicao", width=350)

        scroll = ctk.CTkScrollbar(area_tabela, command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll.set)

        self.tabela.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scroll.pack(side="right", fill="y", padx=(0, 4), pady=8)

        self.tabela.bind("<<TreeviewSelect>>", self.ao_selecionar)

    def _ao_trocar_modo_condicao(self, modo):
        if modo == MODO_AUDIO:
            self.duracao_condicao.pack(side="left", padx=(8, 0))
            self.btn_audio_condicao.pack(side="left", padx=(8, 0))
        else:
            self.duracao_condicao.pack_forget()
            self.btn_audio_condicao.pack_forget()

    def gravar_audio_condicao(self):
        if self._gravacao_condicao_em_andamento:
            return

        try:
            duracao = int(self.duracao_condicao.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Informe a duração em segundos.")
            return

        if not 1 <= duracao <= MAX_DURACAO_AUDIO:
            messagebox.showwarning(
                "Aviso",
                f"A duração deve estar entre 1 e {MAX_DURACAO_AUDIO} segundos.",
            )
            return

        from services.audio_service import gravar_e_transcrever

        self._gravacao_condicao_em_andamento = True
        self.btn_audio_condicao.configure(state="disabled")
        self.status_audio_condicao.configure(text="Preparando a gravação local...")
        self.status_audio_condicao.pack(side="left", padx=(8, 0))
        Thread(
            target=self._executar_gravacao_condicao,
            args=(gravar_e_transcrever, duracao),
            daemon=True,
        ).start()

    def _executar_gravacao_condicao(self, gravar_e_transcrever, duracao):
        try:
            texto = gravar_e_transcrever(
                duracao,
                progresso=lambda mensagem: self._fila_audio_condicao.put(
                    ("status", mensagem)
                ),
            )
        except AudioServiceError as erro:
            self._fila_audio_condicao.put(("erro", str(erro)))
        else:
            self._fila_audio_condicao.put(("concluido", texto))

    def _processar_fila_audio_condicao(self):
        while True:
            try:
                estado, conteudo = self._fila_audio_condicao.get_nowait()
            except Empty:
                break

            if estado == "status":
                self.status_audio_condicao.configure(text=conteudo)
                continue

            self._gravacao_condicao_em_andamento = False
            self.btn_audio_condicao.configure(state="normal")
            if estado == "erro":
                self.status_audio_condicao.configure(
                    text="Não foi possível gravar o áudio."
                )
                messagebox.showerror("Erro no áudio", conteudo)
            else:
                self.condicao.delete(0, "end")
                self.condicao.insert(0, conteudo)
                self.status_audio_condicao.configure(
                    text="Transcrição pronta. Revise antes de salvar."
                )

        if self.root.winfo_exists():
            self.root.after(100, self._processar_fila_audio_condicao)


    # ------------------------------------------------------------------
    # TEMA
    # ------------------------------------------------------------------
    def alternar_tema(self):
        modo = "dark" if self.switch_tema.get() == 1 else "light"
        ctk.set_appearance_mode(modo)
        self.aplicar_estilo_tabela()

    def aplicar_estilo_tabela(self):
        """A Treeview é do tkinter puro, então precisa ser recolorida à mão."""
        c = CORES_TABELA[ctk.get_appearance_mode()]
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Acolhe.Treeview",
            background=c["bg"], fieldbackground=c["bg"], foreground=c["fg"],
            rowheight=30, borderwidth=0, font=("Arial", 11),
        )
        estilo.configure(
            "Acolhe.Treeview.Heading",
            background=c["cab_bg"], foreground=c["cab_fg"],
            font=("Arial", 11, "bold"), relief="flat",
        )
        estilo.map(
            "Acolhe.Treeview",
            background=[("selected", c["sel"])],
            foreground=[("selected", "#FFFFFF")],
        )
        estilo.map("Acolhe.Treeview.Heading", background=[("active", c["cab_bg"])])

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def atualizar_lista(self):
        """READ: recarrega a tabela (respeitando o texto da busca)."""
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for paciente in PacienteRepository.listar(self.busca.get().strip()):
            self.tabela.insert("", "end", values=paciente)

    def ao_selecionar(self, _evento=None):
        """Clicou numa linha: carrega os dados no formulário para editar."""
        selecao = self.tabela.selection()
        if not selecao:
            return

        id_, nome, condicao = self.tabela.item(selecao[0], "values")
        self.paciente_selecionado = int(id_)

        self.nome.delete(0, "end")
        self.nome.insert(0, nome)
        self.condicao.delete(0, "end")
        self.condicao.insert(0, condicao)

        self.lbl_modo.configure(text=f"Editando paciente #{id_}")
        self.btn_salvar.configure(text="Atualizar")
        self.btn_excluir.configure(state="normal")

    def salvar(self):
        """CREATE (novo) ou UPDATE (se há paciente selecionado)."""
        nome = self.nome.get().strip()
        condicao = self.condicao.get().strip()

        if not nome or not condicao:
            messagebox.showwarning("Aviso", "Preencha o nome e a condição.")
            return

        if self.paciente_selecionado is None:
            PacienteRepository.salvar(nome, condicao)
        else:
            PacienteRepository.atualizar(self.paciente_selecionado, nome, condicao)

        self.limpar_formulario()
        self.atualizar_lista()
        self._sincronizar_consultas()

    def excluir(self):
        """DELETE: pede confirmação antes de apagar."""
        if self.paciente_selecionado is None:
            return

        if not messagebox.askyesno(
            "Confirmar exclusão", "Deseja realmente excluir este paciente?"
        ):
            return

        PacienteRepository.excluir(self.paciente_selecionado)
        self.limpar_formulario()
        self.atualizar_lista()
        self._sincronizar_consultas()

    def abrir_consultas(self):
        if self.janela_consultas is not None and self.janela_consultas.winfo_exists():
            self.janela_consultas.focus()
            return

        self.janela_consultas = ctk.CTkToplevel(self.root)
        self.janela_consultas.title("AcolheMind - Consultas")
        self.janela_consultas.geometry("900x650")

        sistema = SistemaAcolheMind(BaseConhecimento(["Validação local"]))
        sistema.sincronizar_pacientes(PacienteRepository.listar())
        self.consulta_frame = ConsultaFrame(
            self.janela_consultas, sistema, ModeradorClinico()
        )
        self.consulta_frame.pack(fill="both", expand=True, padx=16, pady=16)

    def _sincronizar_consultas(self):
        if (
            self.consulta_frame is not None
            and self.janela_consultas is not None
            and self.janela_consultas.winfo_exists()
        ):
            self.consulta_frame.sistema.sincronizar_pacientes(
                PacienteRepository.listar()
            )
            self.consulta_frame.atualizar_pacientes()

    # ------------------------------------------------------------------
    # ADMINISTRADOR
    # ------------------------------------------------------------------
    def exportar(self):
        """Gera a planilha Excel completa (pacientes + consultas)."""
        caminho = filedialog.asksaveasfilename(
            title="Salvar planilha",
            defaultextension=".xlsx",
            initialfile=f"acolhemind_{datetime.now():%Y-%m-%d}.xlsx",
            filetypes=[("Planilha Excel", "*.xlsx")],
        )
        if not caminho:
            return

        try:
            exportar_excel(caminho)
        except PermissionError:
            messagebox.showerror(
                "Erro", "Não foi possível salvar. Feche a planilha se ela estiver aberta."
            )
            return

        messagebox.showinfo(
            "Exportado",
            "Planilha salva com sucesso.\n\n"
            "Atenção: ela contém dados sensíveis de saúde. "
            "Guarde em local seguro.",
        )

    def sair(self):
        self.voltar_ao_login = True
        self.root.destroy()

    def limpar_formulario(self):
        self.paciente_selecionado = None
        self.nome.delete(0, "end")
        self.condicao.delete(0, "end")
        self.modo_condicao.set(MODO_TEXTO)
        self._ao_trocar_modo_condicao(MODO_TEXTO)
        self.duracao_condicao.delete(0, "end")
        self.duracao_condicao.insert(0, "5")
        self.tabela.selection_remove(self.tabela.selection())
        self.lbl_modo.configure(text="Novo paciente")
        self.btn_salvar.configure(text="Salvar")
        self.btn_excluir.configure(state="disabled")
        self.root.focus()

    def executar(self):
        self.root.mainloop()
