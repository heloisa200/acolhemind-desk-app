from queue import Empty, Queue
from threading import Thread
from tkinter import messagebox, ttk

import customtkinter as ctk

from gui import tema
from repositories.paciente_repository import PacienteRepository
from services.audio_service import AudioServiceError

MODO_TEXTO = "Texto"
MODO_AUDIO = "Áudio (português)"
MAX_DURACAO_AUDIO = 300


class PacienteWindow:
    """Área do paciente: nome, condição (texto ou áudio), CRUD e troca de tema.

    Por privacidade, a tabela mostra APENAS os registros feitos nesta sessão.
    Os registros completos só aparecem no painel do administrador.
    """

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AcolheMind - Área do Paciente")
        self.root.geometry("920x700")

        self.registro_selecionado = None  # id em edição (None = novo registro)
        self.ids_sessao = []              # ids criados nesta sessão
        self._fila_audio = Queue()
        self._gravacao_em_andamento = False

        self.criar_tela()
        tema.aplicar_estilo_tabela()
        self.atualizar_lista()
        self.root.after(100, self._processar_fila_audio)

    # ------------------------------------------------------------------
    # INTERFACE
    # ------------------------------------------------------------------
    def criar_tela(self):
        # ----- Cabeçalho: título + botão de tema -----
        topo = ctk.CTkFrame(self.root, fg_color="transparent")
        topo.pack(fill="x", padx=20, pady=(15, 0))

        ctk.CTkLabel(
            topo,
            text="AcolheMind - Área do Paciente",
            font=("Arial", 24, "bold"),
        ).pack(side="left")

        self.switch_tema = tema.criar_switch_tema(topo, tema.aplicar_estilo_tabela)
        self.switch_tema.pack(side="right")

        barra = ctk.CTkFrame(self.root, fg_color="transparent")
        barra.pack(fill="x", padx=20, pady=(2, 0))

        ctk.CTkLabel(
            barra,
            text="Os registros completos só podem ser vistos pelo administrador.",
            text_color="gray50",
        ).pack(side="left")

        ctk.CTkButton(
            barra, text="Voltar ao menu", width=130,
            fg_color="gray50", hover_color="gray35",
            command=self.voltar,
        ).pack(side="right")

        
        form = ctk.CTkFrame(self.root)
        form.pack(fill="x", padx=20, pady=10)

        self.lbl_modo = ctk.CTkLabel(
            form, text="Novo registro", font=("Arial", 14, "bold")
        )
        self.lbl_modo.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 0))

        self.nome = ctk.CTkEntry(form, width=360, placeholder_text="Seu nome")
        self.nome.grid(row=1, column=0, padx=15, pady=10)

        self.condicao = ctk.CTkEntry(form, width=360, placeholder_text="Sua condição")
        self.condicao.grid(row=1, column=1, padx=15, pady=10)

        # ----- Relato por texto ou áudio -----
        linha_modo = ctk.CTkFrame(form, fg_color="transparent")
        linha_modo.grid(row=2, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 8))

        ctk.CTkLabel(linha_modo, text="Relatar por:").pack(side="left")
        self.modo = ctk.CTkOptionMenu(
            linha_modo,
            values=[MODO_TEXTO, MODO_AUDIO],
            command=self._ao_trocar_modo,
            width=170,
        )
        self.modo.pack(side="left", padx=(8, 0))

        self.duracao = ctk.CTkEntry(linha_modo, width=110, placeholder_text="Segundos")
        self.duracao.insert(0, "5")
        self.btn_audio = ctk.CTkButton(
            linha_modo, text="Gravar áudio", width=120, command=self.gravar_audio
        )
        self.status_audio = ctk.CTkLabel(linha_modo, text="", text_color="gray50")

       
        botoes = ctk.CTkFrame(form, fg_color="transparent")
        botoes.grid(row=3, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 6))

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

        self.status = ctk.CTkLabel(form, text="", anchor="w", text_color="gray50")
        self.status.grid(row=4, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 10))

      
        ctk.CTkLabel(
            self.root,
            text="Registros feitos nesta sessão (só você vê esta lista)",
            font=("Arial", 13, "bold"),
        ).pack(anchor="w", padx=20, pady=(4, 4))

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
        self.tabela.column("nome", width=330)
        self.tabela.column("condicao", width=330)

        scroll = ctk.CTkScrollbar(area_tabela, command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll.set)

        self.tabela.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scroll.pack(side="right", fill="y", padx=(0, 4), pady=8)

        self.tabela.bind("<<TreeviewSelect>>", self.ao_selecionar)

    def voltar(self):
        self.root.destroy()

    
    def atualizar_lista(self):
        """READ: mostra só os registros desta sessão."""
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for registro in PacienteRepository.listar_por_ids(self.ids_sessao):
            self.tabela.insert("", "end", values=registro)

    def ao_selecionar(self, _evento=None):
        """Clicou numa linha: carrega os dados no formulário para editar."""
        selecao = self.tabela.selection()
        if not selecao:
            return

        id_, nome, condicao = self.tabela.item(selecao[0], "values")
        if int(id_) not in self.ids_sessao:
            return
        self.registro_selecionado = int(id_)

        self.nome.delete(0, "end")
        self.nome.insert(0, nome)
        self.condicao.delete(0, "end")
        self.condicao.insert(0, condicao)

        self.lbl_modo.configure(text=f"Editando registro #{id_}")
        self.btn_salvar.configure(text="Atualizar")
        self.btn_excluir.configure(state="normal")
        self.status.configure(text="")

    def salvar(self):
        """CREATE (novo) ou UPDATE (se há registro selecionado)."""
        nome = self.nome.get().strip()
        condicao = self.condicao.get().strip()

        if not nome or not condicao:
            messagebox.showwarning("Aviso", "Preencha o nome e a condição.")
            return

        if self.registro_selecionado is None:
            novo_id = PacienteRepository.salvar(nome, condicao)
            self.ids_sessao.append(novo_id)
            mensagem = "Registro salvo."
        else:
            if self.registro_selecionado not in self.ids_sessao:
                self.limpar_formulario()
                return
            PacienteRepository.atualizar(self.registro_selecionado, nome, condicao)
            mensagem = "Registro atualizado."

        self.limpar_formulario()
        self.atualizar_lista()
        self.status.configure(text=mensagem)

    def excluir(self):
        """DELETE: pede confirmação antes de apagar."""
        if self.registro_selecionado not in self.ids_sessao:
            return

        if not messagebox.askyesno(
            "Confirmar exclusão", "Deseja realmente excluir este registro?"
        ):
            return

        PacienteRepository.excluir(self.registro_selecionado)
        self.ids_sessao.remove(self.registro_selecionado)

        self.limpar_formulario()
        self.atualizar_lista()
        self.status.configure(text="Registro excluído.")

    def limpar_formulario(self):
        self.registro_selecionado = None
        self.nome.delete(0, "end")
        self.condicao.delete(0, "end")
        self.modo.set(MODO_TEXTO)
        self._ao_trocar_modo(MODO_TEXTO)
        self.duracao.delete(0, "end")
        self.duracao.insert(0, "5")
        self.status_audio.configure(text="")
        self.status.configure(text="")
        self.tabela.selection_remove(self.tabela.selection())
        self.lbl_modo.configure(text="Novo registro")
        self.btn_salvar.configure(text="Salvar")
        self.btn_excluir.configure(state="disabled")
        self.root.focus()

   
    def _ao_trocar_modo(self, modo):
        if modo == MODO_AUDIO:
            self.duracao.pack(side="left", padx=(8, 0))
            self.btn_audio.pack(side="left", padx=(8, 0))
        else:
            self.duracao.pack_forget()
            self.btn_audio.pack_forget()
            self.status_audio.pack_forget()

    def gravar_audio(self):
        if self._gravacao_em_andamento:
            return

        try:
            duracao = int(self.duracao.get())
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

        self._gravacao_em_andamento = True
        self.btn_audio.configure(state="disabled")
        self.status_audio.configure(text="Preparando a gravação local...")
        self.status_audio.pack(side="left", padx=(8, 0))
        Thread(
            target=self._executar_gravacao,
            args=(gravar_e_transcrever, duracao),
            daemon=True,
        ).start()

    def _executar_gravacao(self, gravar_e_transcrever, duracao):
        try:
            texto = gravar_e_transcrever(
                duracao,
                progresso=lambda mensagem: self._fila_audio.put(("status", mensagem)),
            )
        except AudioServiceError as erro:
            self._fila_audio.put(("erro", str(erro)))
        else:
            self._fila_audio.put(("concluido", texto))

    def _processar_fila_audio(self):
        while True:
            try:
                estado, conteudo = self._fila_audio.get_nowait()
            except Empty:
                break

            if estado == "status":
                self.status_audio.configure(text=conteudo)
                continue

            self._gravacao_em_andamento = False
            self.btn_audio.configure(state="normal")
            if estado == "erro":
                self.status_audio.configure(text="Não foi possível gravar o áudio.")
                messagebox.showerror("Erro no áudio", conteudo)
            else:
                self.condicao.delete(0, "end")
                self.condicao.insert(0, conteudo)
                self.status_audio.configure(
                    text="Transcrição pronta. Revise antes de salvar."
                )

        if self.root.winfo_exists():
            self.root.after(100, self._processar_fila_audio)

    def executar(self):
        self.root.mainloop()
