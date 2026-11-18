import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from typing import Dict, List

# 1. CAMADA DE MODELAGEM (ORIENTAÇÃO A OBJETOS)

class EntradaRelato(ABC):
    """Classe base abstrata para Herança e Polimorfismo."""
    def __init__(self, conteudo: str):
        self.conteudo = conteudo

    @abstractmethod
    def extrair_sintomas(self) -> str:
        pass

class RelatoTexto(EntradaRelato):
    def extrair_sintomas(self) -> str:
        return f"[Texto]: {self.conteudo}"

class RelatoAudio(EntradaRelato):
    def __init__(self, conteudo: str, duracao_segundos: int):
        super().__init__(conteudo)
        self.duracao_segundos = duracao_segundos

    def extrair_sintomas(self) -> str:
        return f"[Áudio transcrito - {self.duracao_segundos}s]: {self.conteudo}"

class BaseConhecimento:
    """Relação de Associação (Agregação) com o sistema."""
    def __init__(self, manuais: List[str]):
        self.manuais = manuais

    def consultar_diretrizes(self) -> str:
        return f"Validado via: {', '.join(self.manuais)}"

class ModeradorClinico:
    """Relação de Dependência no processamento."""
    def validar_seguranca(self, texto: str) -> bool:
        return len(texto.strip()) > 2

class Paciente:
    """Relação de Associação 1 para N com o sistema."""
    def __init__(self, nome: str, id_perfil: str, neuroatipicidade: str):
        self.nome = nome
        self.id_perfil = id_perfil
        self.neuroatipicidade = neuroatipicidade

    def exibir_perfil(self) -> str:
        return f"Paciente: {self.nome} ({self.id_perfil}) | Condição: {self.neuroatipicidade}"

class RelatorioClinico:
    """Relação de Composição: nasce e morre dentro da sessão do sistema."""
    def __init__(self, motivo_consulta: str):
        self.motivo_consulta = motivo_consulta
        self.sintomas_principais: List[str] = []
        self.gatilhos_sobrecarga: List[str] = []

    def adicionar_dados(self, sintoma: str, gatilho: str):
        if sintoma:
            self.sintomas_principais.append(sintoma)
        if gatilho and gatilho not in self.gatilhos_sobrecarga:
            self.gatilhos_sobrecarga.append(gatilho)

    def gerar_texto_resumo(self, paciente: Paciente, validacao_rag: str) -> str:
        sintomas_fmt = "\n  - ".join(self.sintomas_principais) if self.sintomas_principais else "Nenhum registrado"
        gatilhos_fmt = ", ".join(self.gatilhos_sobrecarga) if self.gatilhos_sobrecarga else "Nenhum informado"
        
        return (
            "====================================================\n"
            "   RESUMO CLÍNICO OBJETIVO (LEITURA MÉDICA < 30s)   \n"
            "====================================================\n"
            f"• {paciente.exibir_perfil()}\n"
            f"• Motivo da Consulta: {self.motivo_consulta}\n\n"
            "• Sintomas Principais:\n"
            f"  - {sintomas_fmt}\n\n"
            f"• Gatilhos de Sobrecarga: {gatilhos_fmt}\n"
            "----------------------------------------------------\n"
            f"Status RAG: {validacao_rag}\n"
            "===================================================="
        )

class SistemaAcolheMind:
    def __init__(self, base_dados: BaseConhecimento):
        self.base_conhecimento = base_dados
        self.pacientes_cadastrados: Dict[str, Paciente] = {}
        self.sessao_relatorio: RelatorioClinico = None

    def cadastrar_paciente(self, nome: str, id_perfil: str, neuroatipicidade: str) -> Paciente:
        novo = Paciente(nome, id_perfil, neuroatipicidade)
        self.pacientes_cadastrados[id_perfil] = novo
        return novo

    def iniciar_sessao_consulta(self, motivo_consulta: str):
        self.sessao_relatorio = RelatorioClinico(motivo_consulta)

    def processar_interacao(self, entrada: EntradaRelato, moderador: ModeradorClinico, gatilho: str) -> bool:
        texto_processado = entrada.extrair_sintomas()
        if moderador.validar_seguranca(entrada.conteudo) and self.sessao_relatorio:
            self.sessao_relatorio.adicionar_dados(texto_processado, gatilho)
            return True
        return False
      
# 2. CAMADA VISUAL (INTERFACE DESKTOP TKINTER)
class AcolheMindAppGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AcolheMind - Assistente Pré-Consulta (Desktop)")
        self.root.geometry("760x680")
        self.root.configure(bg="#F4F6F9")

        manuais = ["Manual TEA 2026", "Guia de Acessibilidade em Saúde"]
        self.base_rag = BaseConhecimento(manuais)
        self.moderador = ModeradorClinico()
        self.sistema = SistemaAcolheMind(base_dados=self.base_rag)
        self.perfil_atual_id = "perfil_principal"

        self._construir_interface()

    def _construir_interface(self):
        header = tk.Frame(self.root, bg="#2B5B84", pady=12)
        header.pack(fill="x")
        tk.Label(
            header, text="AcolheMind — Suporte Pré-Consulta Neurodivergente",
            font=("Arial", 14, "bold"), fg="white", bg="#2B5B84"
        ).pack()

        container = tk.Frame(self.root, bg="#F4F6F9", padx=20, pady=10)
        container.pack(fill="both", expand=True)

        # BLOCO 1: CADASTRO DO PACIENTE
        frame_pac = tk.LabelFrame(container, text=" 1. Perfil do Paciente ", font=("Arial", 10, "bold"), bg="#F4F6F9", padx=10, pady=8)
        frame_pac.pack(fill="x", pady=5)

        tk.Label(frame_pac, text="Nome:", bg="#F4F6F9").grid(row=0, column=0, sticky="w")
        self.ent_nome = tk.Entry(frame_pac, width=28)
        self.ent_nome.insert(0, "Heloisa Alves")
        self.ent_nome.grid(row=0, column=1, padx=5)

        tk.Label(frame_pac, text="Condição:", bg="#F4F6F9").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.ent_condicao = tk.Entry(frame_pac, width=22)
        self.ent_condicao.insert(0, "TEA / TDAH")
        self.ent_condicao.grid(row=0, column=3, padx=5)

        btn_salvar_pac = tk.Button(frame_pac, text="Salvar Perfil", bg="#4CAF50", fg="white", command=self.acao_cadastrar_paciente)
        btn_salvar_pac.grid(row=0, column=4, padx=10)

        # BLOCO 2: SESSÃO E RELATO MULTIMODAL
        frame_rel = tk.LabelFrame(container, text=" 2. Organização de Sintomas e Gatilhos ", font=("Arial", 10, "bold"), bg="#F4F6F9", padx=10, pady=8)
        frame_rel.pack(fill="x", pady=5)

        tk.Label(frame_rel, text="Motivo da Consulta:", bg="#F4F6F9").grid(row=0, column=0, sticky="w")
        self.ent_motivo = tk.Entry(frame_rel, width=55)
        self.ent_motivo.insert(0, "Check-up cardiológico anual")
        self.ent_motivo.grid(row=0, column=1, columnspan=2, sticky="w", pady=4)

        tk.Label(frame_rel, text="Modo de Entrada:", bg="#F4F6F9").grid(row=1, column=0, sticky="w")
        self.tipo_entrada = ttk.Combobox(frame_rel, values=["Texto", "Áudio (Simulado)"], state="readonly", width=20)
        self.tipo_entrada.current(0)
        self.tipo_entrada.grid(row=1, column=1, sticky="w", pady=4)

        tk.Label(frame_rel, text="Descreva o Sintoma:", bg="#F4F6F9").grid(row=2, column=0, sticky="w")
        self.ent_sintoma = tk.Entry(frame_rel, width=55)
        self.ent_sintoma.insert(0, "Palpitações fortes e falta de ar após viagem.")
        self.ent_sintoma.grid(row=2, column=1, columnspan=2, sticky="w", pady=4)

        tk.Label(frame_rel, text="Gatilho Sensorial:", bg="#F4F6F9").grid(row=3, column=0, sticky="w")
        self.ent_gatilho = tk.Entry(frame_rel, width=55)
        self.ent_gatilho.insert(0, "Luz fluorescente forte e sala de espera barulhenta")
        self.ent_gatilho.grid(row=3, column=1, columnspan=2, sticky="w", pady=4)

        frame_botoes = tk.Frame(frame_rel, bg="#F4F6F9")
        frame_botoes.grid(row=4, column=0, columnspan=3, pady=8)

        tk.Button(
            frame_botoes, text="+ Adicionar Sintoma ao Relatório", bg="#2B5B84", fg="white",
            command=self.acao_adicionar_relato
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes, text="🌬️ Exercício de Respiração", bg="#FF9800", fg="white",
            command=self.acao_respiracao
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes, text="📄 Gerar Resumo Clínico", bg="#00897B", fg="white",
            command=self.acao_gerar_relatorio
        ).pack(side="left", padx=5)

        # BLOCO 3: VISUALIZAÇÃO DO RELATÓRIO (< 30 SEGUNDOS)
        frame_out = tk.LabelFrame(container, text=" 3. Relatório Clínico Estruturado (Visão Médica) ", font=("Arial", 10, "bold"), bg="#F4F6F9", padx=10, pady=8)
        frame_out.pack(fill="both", expand=True, pady=5)

        self.txt_relatorio = tk.Text(frame_out, height=13, font=("Courier New", 10), bg="#FFFFFF", fg="#222222")
        self.txt_relatorio.pack(fill="both", expand=True)

        self.acao_cadastrar_paciente(silencioso=True)

    def acao_cadastrar_paciente(self, silencioso=False):
        nome = self.ent_nome.get().strip()
        condicao = self.ent_condicao.get().strip()
        if not nome or not condicao:
            messagebox.showwarning("Aviso", "Preencha o nome e a condição do paciente.")
            return
        self.sistema.cadastrar_paciente(nome, self.perfil_atual_id, condicao)
        if not silencioso:
            messagebox.showinfo("Sucesso", f"Perfil de {nome} atualizado com sucesso!")

    def acao_adicionar_relato(self):
        motivo = self.ent_motivo.get().strip()
        sintoma = self.ent_sintoma.get().strip()
        gatilho = self.ent_gatilho.get().strip()
        modo = self.tipo_entrada.get()

        if self.sistema.sessao_relatorio is None or self.sistema.sessao_relatorio.motivo_consulta != motivo:
            self.sistema.iniciar_sessao_consulta(motivo)


