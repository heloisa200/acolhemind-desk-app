import customtkinter as ctk

from gui import tema


class HomeWindow:
    """Página inicial: o usuário escolhe entrar como paciente ou administrador."""

    def __init__(self):
        self.escolha = None  # "paciente", "admin" ou None (fechou a janela)

        self.root = ctk.CTk()
        self.root.title("AcolheMind")
        self.root.geometry("560x580")
        self.root.resizable(False, False)

        self.criar_tela()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def criar_tela(self):
        topo = ctk.CTkFrame(self.root, fg_color="transparent")
        topo.pack(fill="x", padx=20, pady=(15, 0))
        tema.criar_switch_tema(topo).pack(side="right")

        ctk.CTkLabel(
            self.root, text="AcolheMind", font=("Arial", 38, "bold")
        ).pack(pady=(30, 4))
        ctk.CTkLabel(
            self.root,
            text="Acolhimento e cuidado com você",
            font=("Arial", 15),
            text_color="gray50",
        ).pack(pady=(0, 36))

        # --Paciente --
        ctk.CTkButton(
            self.root,
            text="Acessar como paciente",
            width=360,
            height=64,
            font=("Arial", 18, "bold"),
            command=lambda: self.escolher("paciente"),
        ).pack()
        ctk.CTkLabel(
            self.root,
            text="Informe seu nome e sua condição, por texto ou por áudio.",
            font=("Arial", 12),
            text_color="gray50",
        ).pack(pady=(6, 28))

        # - Administrador -
        ctk.CTkButton(
            self.root,
            text="Acessar como administrador",
            width=360,
            height=64,
            font=("Arial", 18, "bold"),
            fg_color="#3B5B7A",
            hover_color="#2D465E",
            command=lambda: self.escolher("admin"),
        ).pack()
        ctk.CTkLabel(
            self.root,
            text="Acesso restrito, com usuário e senha.",
            font=("Arial", 12),
            text_color="gray50",
        ).pack(pady=(6, 0))

        ctk.CTkLabel(
            self.root,
            text="Os registros completos só podem ser vistos pelo administrador.",
            font=("Arial", 11),
            text_color="gray50",
        ).pack(side="bottom", pady=(0, 18))

    def escolher(self, opcao):
        self.escolha = opcao
        self.root.destroy()

    def executar(self):
        """Mostra o menu e devolve "paciente", "admin" ou None."""
        self.root.mainloop()
        return self.escolha
