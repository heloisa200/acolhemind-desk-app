from tkinter import filedialog, messagebox
from queue import Empty, Queue
from threading import Thread

import customtkinter as ctk

from models.entrada_relato import RelatoAudio, RelatoTexto
from repositories.consulta_repository import ConsultaRepository
from services.audio_service import AudioServiceError

MODO_TEXTO = "Texto"
MODO_AUDIO = "Áudio (transcrição em português)"
SEM_PACIENTE = "Nenhum paciente cadastrado"
MAX_DURACAO_AUDIO = 300


class ConsultaFrame(ctk.CTkFrame):
    """Aba de consulta: monta o RelatorioClinico usando as classes do UML."""

    def __init__(self, master, sistema, moderador):
        super().__init__(master, fg_color="transparent")

        self.sistema = sistema        # SistemaAcolheMind
        self.moderador = moderador    # ModeradorClinico
        self.sessao_paciente_id = None
        self.mapa_pacientes = {}      # "1 - Nome" -> "1"
        self.ultimo_resumo = ""
        self._fila_audio = Queue()
        self._gravacao_em_andamento = False

        self._criar_tela()
        self.atualizar_pacientes()
        self.after(100, self._processar_fila_audio)

    # ------------------------------------------------------------------
    # INTERFACE
    # ------------------------------------------------------------------
    def _criar_tela(self):
        form = ctk.CTkFrame(self)
        form.pack(fill="x", pady=(0, 8))
        form.grid_columnconfigure(1, weight=1)

        def rotulo(linha, texto):
            ctk.CTkLabel(form, text=texto).grid(
                row=linha, column=0, sticky="w", padx=(15, 10), pady=6
            )

        rotulo(0, "Paciente:")
        self.combo = ctk.CTkComboBox(form, values=[""], state="readonly")
        self.combo.grid(row=0, column=1, sticky="ew", padx=(0, 15), pady=6)

        rotulo(1, "Motivo da consulta:")
        self.motivo = ctk.CTkEntry(form, placeholder_text="Ex.: Check-up anual")
        self.motivo.grid(row=1, column=1, sticky="ew", padx=(0, 15), pady=6)

        rotulo(2, "Modo de entrada:")
        linha_modo = ctk.CTkFrame(form, fg_color="transparent")
        linha_modo.grid(row=2, column=1, sticky="w", pady=6)
        self.modo = ctk.CTkOptionMenu(
            linha_modo,
            values=[MODO_TEXTO, MODO_AUDIO],
            command=self._ao_trocar_modo,
            width=180,
        )
        self.modo.pack(side="left")
        self.duracao = ctk.CTkEntry(
            linha_modo, width=110, placeholder_text="Duração (s)"
        )
        self.duracao.insert(0, "5")
        self.btn_audio = ctk.CTkButton(
            linha_modo, text="Gravar áudio", width=120, command=self.gravar_audio
        )

        rotulo(3, "Sintoma:")
        self.sintoma = ctk.CTkEntry(
            form, placeholder_text="Descreva o sintoma"
        )
        self.sintoma.grid(row=3, column=1, sticky="ew", padx=(0, 15), pady=6)

        rotulo(4, "Gatilho sensorial:")
        self.gatilho = ctk.CTkEntry(
            form, placeholder_text="Ex.: luz forte, sala barulhenta"
        )
        self.gatilho.grid(row=4, column=1, sticky="ew", padx=(0, 15), pady=6)

        botoes = ctk.CTkFrame(form, fg_color="transparent")
        botoes.grid(row=5, column=0, columnspan=2, sticky="w", padx=15, pady=(4, 12))

        ctk.CTkButton(
            botoes, text="+ Adicionar ao relatório", command=self.adicionar
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            botoes, text="Gerar resumo clínico",
            fg_color="#00897B", hover_color="#00695C",
            command=self.gerar_resumo,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            botoes, text="Salvar PDF",
            fg_color="#1D7A46", hover_color="#155B34",
            command=self.salvar_pdf,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            botoes, text="Nova sessão",
            fg_color="gray50", hover_color="gray35",
            command=self.nova_sessao,
        ).pack(side="left")

        self.status = ctk.CTkLabel(self, text="", anchor="w", text_color="gray50")
        self.status.pack(fill="x", padx=4)

        self.saida = ctk.CTkTextbox(self, font=("Courier New", 13), wrap="none")
        self.saida.pack(fill="both", expand=True, pady=(4, 0))
        self.saida.configure(state="disabled")

    def _ao_trocar_modo(self, modo):
        if modo == MODO_AUDIO:
            self.duracao.pack(side="left", padx=(10, 0))
            self.btn_audio.pack(side="left", padx=(10, 0))
        else:
            self.duracao.pack_forget()
            self.btn_audio.pack_forget()

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
        self.status.configure(text="Preparando a gravação local...")
        Thread(
            target=self._executar_gravacao,
            args=(gravar_e_transcrever, duracao),
            daemon=True,
        ).start()

    def _executar_gravacao(self, gravar_e_transcrever, duracao):
        try:
            texto = gravar_e_transcrever(
                duracao,
                progresso=lambda mensagem: self._fila_audio.put(
                    ("status", mensagem)
                ),
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
                self.status.configure(text=conteudo)
                continue

            self._gravacao_em_andamento = False
            self.btn_audio.configure(state="normal")
            if estado == "erro":
                self.status.configure(text="Não foi possível gravar o áudio.")
                messagebox.showerror("Erro no áudio", conteudo)
            else:
                self.sintoma.delete(0, "end")
                self.sintoma.insert(0, conteudo)
                self.status.configure(
                    text="Transcrição pronta. Revise o texto antes de adicionar."
                )

        if self.winfo_exists():
            self.after(100, self._processar_fila_audio)

    # ------------------------------------------------------------------
    # PACIENTES
    # ------------------------------------------------------------------
    def atualizar_pacientes(self):
        """Chamado quando a lista de pacientes muda (aba Pacientes)."""
        pacientes = sorted(
            self.sistema.pacientes_cadastrados.values(),
            key=lambda p: int(p.id_perfil),
        )
        self.mapa_pacientes = {
            f"{p.id_perfil} - {p.nome}": p.id_perfil for p in pacientes
        }
        rotulos = list(self.mapa_pacientes)

        if rotulos:
            self.combo.configure(values=rotulos)
            if self.combo.get() not in rotulos:
                self.combo.set(rotulos[0])
        else:
            self.combo.configure(values=[SEM_PACIENTE])
            self.combo.set(SEM_PACIENTE)

        # Paciente da sessão foi excluído: encerra a sessão
        if (
            self.sessao_paciente_id is not None
            and self.sessao_paciente_id not in self.sistema.pacientes_cadastrados
        ):
            self.nova_sessao()

    def _paciente_atual(self):
        id_perfil = self.mapa_pacientes.get(self.combo.get())
        return self.sistema.pacientes_cadastrados.get(id_perfil)

    # ------------------------------------------------------------------
    # AÇÕES
    # ------------------------------------------------------------------
    def adicionar(self):
        paciente = self._paciente_atual()
        if paciente is None:
            messagebox.showwarning("Aviso", "Cadastre e selecione um paciente.")
            return

        motivo = self.motivo.get().strip()
        sintoma = self.sintoma.get().strip()
        gatilho = self.gatilho.get().strip()

        if not motivo or not sintoma:
            messagebox.showwarning("Aviso", "Preencha o motivo e o sintoma.")
            return

        # Polimorfismo: texto e áudio são tratados como EntradaRelato
        if self.modo.get() == MODO_AUDIO:
            try:
                duracao = int(self.duracao.get())
                if duracao <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    "Aviso", "Informe a duração do áudio em segundos (número)."
                )
                return
            entrada = RelatoAudio(sintoma, duracao)
            origem = f"Áudio {duracao}s"
        else:
            entrada = RelatoTexto(sintoma)
            origem = "Texto"

        # Nova sessão se mudou o paciente ou o motivo
        sessao = self.sistema.sessao_relatorio
        if (
            sessao is None
            or sessao.motivo_consulta != motivo
            or self.sessao_paciente_id != paciente.id_perfil
        ):
            self.sistema.iniciar_sessao_consulta(motivo)
            self.sessao_paciente_id = paciente.id_perfil
            self._mostrar("")

        if not self.sistema.processar_interacao(entrada, self.moderador, gatilho):
            messagebox.showwarning(
                "Aviso", "Relato muito curto. Descreva com mais detalhes."
            )
            return

        # Guarda no banco (aparece na aba "Consultas" da planilha Excel)
        observacao = f"[{origem}] Gatilho: {gatilho}" if gatilho else f"[{origem}]"
        ConsultaRepository.salvar(int(paciente.id_perfil), motivo, sintoma, observacao)

        total = len(self.sistema.sessao_relatorio.sintomas_principais)
        self.status.configure(text=f"Sintoma adicionado. Itens no relatório: {total}")
        self.sintoma.delete(0, "end")
        self.gatilho.delete(0, "end")

    def gerar_resumo(self):
        sessao = self.sistema.sessao_relatorio
        if sessao is None or not sessao.sintomas_principais:
            messagebox.showwarning("Aviso", "Adicione ao menos um sintoma primeiro.")
            return

        self.ultimo_resumo = self.sistema.gerar_resumo(self.sessao_paciente_id)
        self._mostrar(self.ultimo_resumo)
        self.status.configure(text="Resumo gerado.")

    def salvar_pdf(self):
        if not self.ultimo_resumo:
            messagebox.showwarning("Aviso", "Gere o resumo clínico primeiro.")
            return

        try:
            from services.pdf_service import gerar_pdf
        except ModuleNotFoundError:
            messagebox.showerror(
                "Falta um pacote",
                "Para salvar PDF instale o reportlab:\n\npip install reportlab",
            )
            return

        caminho = filedialog.asksaveasfilename(
            title="Salvar resumo em PDF",
            defaultextension=".pdf",
            initialfile="resumo_clinico.pdf",
            filetypes=[("PDF", "*.pdf")],
        )
        if not caminho:
            return

        try:
            gerar_pdf(self.ultimo_resumo, caminho)
        except PermissionError:
            messagebox.showerror(
                "Erro", "Não foi possível salvar. Feche o PDF se ele estiver aberto."
            )
            return

        self.status.configure(text="PDF salvo com sucesso.")

    def nova_sessao(self):
        self.sistema.sessao_relatorio = None
        self.sessao_paciente_id = None
        self.ultimo_resumo = ""
        for campo in (self.motivo, self.sintoma, self.gatilho, self.duracao):
            campo.delete(0, "end")
        self._mostrar("")
        self.status.configure(text="")

    def _mostrar(self, texto):
        self.saida.configure(state="normal")
        self.saida.delete("0.0", "end")
        self.saida.insert("end", texto)
        self.saida.configure(state="disabled")
