import customtkinter as ctk

from services import auth_service

MAX_TENTATIVAS = 5
BLOQUEIO_SEGUNDOS = 30


class LoginWindow:
    """Primeiro acesso: cria o administrador. Depois: pede usuário e senha."""

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AcolheMind - Acesso do Administrador")
        self.root.geometry("460x540")
        self.root.resizable(False, False)

        self.usuario_logado = None
        self.tentativas = 0
        self.primeiro_acesso = not auth_service.existe_admin()

        self.criar_tela()

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.bind("<Return>", lambda e: self.confirmar())

    def criar_tela(self):
        titulo = (
            "Criar administrador" if self.primeiro_acesso else "Acesso restrito"
        )
        ctk.CTkLabel(
            self.root, text="AcolheMind", font=("Arial", 28, "bold")
        ).pack(pady=(30, 0))
        ctk.CTkLabel(
            self.root, text=titulo, font=("Arial", 16)
        ).pack(pady=(0, 20))

        self.usuario = ctk.CTkEntry(self.root, width=300, placeholder_text="Usuário")
        self.usuario.pack(pady=6)

        self.senha = ctk.CTkEntry(
            self.root, width=300, placeholder_text="Senha", show="•"
        )
        self.senha.pack(pady=6)

        self.senha2 = None
        if self.primeiro_acesso:
            self.senha2 = ctk.CTkEntry(
                self.root, width=300, placeholder_text="Repita a senha", show="•"
            )
            self.senha2.pack(pady=6)
            ctk.CTkLabel(
                self.root,
                text="Mínimo de 8 caracteres, com letras e números.",
                font=("Arial", 11),
                text_color="gray50",
            ).pack()

        self.btn = ctk.CTkButton(
            self.root,
            text="Criar e entrar" if self.primeiro_acesso else "Entrar",
            width=300,
            command=self.confirmar,
        )
        self.btn.pack(pady=(18, 8))

        self.msg = ctk.CTkLabel(
            self.root, text="", text_color="#C0392B", wraplength=320
        )
        self.msg.pack(pady=4)

        ctk.CTkButton(
            self.root,
            text="Voltar ao menu",
            width=300,
            fg_color="gray50",
            hover_color="gray35",
            command=self.root.destroy,
        ).pack(pady=(10, 0))

        self.usuario.focus()

    # ------------------------------------------------------------------
    def confirmar(self):
        if str(self.btn.cget("state")) == "disabled":
            return

        usuario = self.usuario.get().strip()
        senha = self.senha.get()

        if not usuario or not senha:
            self.msg.configure(text="Preencha usuário e senha.")
            return

        if self.primeiro_acesso:
            self.criar_admin(usuario, senha)
        else:
            self.entrar(usuario, senha)

    def criar_admin(self, usuario, senha):
        if senha != self.senha2.get():
            self.msg.configure(text="As senhas não conferem.")
            return

        erro = auth_service.validar_senha_nova(senha)
        if erro:
            self.msg.configure(text=erro)
            return

        auth_service.criar_admin(usuario, senha)
        self.sucesso(usuario)

    def entrar(self, usuario, senha):
        if auth_service.autenticar(usuario, senha):
            self.sucesso(usuario)
            return

        self.tentativas += 1
        restantes = MAX_TENTATIVAS - self.tentativas
        self.senha.delete(0, "end")

        if restantes <= 0:
            self.bloquear(BLOQUEIO_SEGUNDOS)
        else:
            self.msg.configure(
                text=f"Usuário ou senha incorretos. Tentativas restantes: {restantes}"
            )

    def bloquear(self, segundos):
        self.btn.configure(state="disabled")
        if segundos > 0:
            self.msg.configure(
                text=f"Muitas tentativas. Aguarde {segundos}s para tentar de novo."
            )
            self.root.after(1000, lambda: self.bloquear(segundos - 1))
        else:
            self.tentativas = 0
            self.msg.configure(text="")
            self.btn.configure(state="normal")

    def sucesso(self, usuario):
        self.usuario_logado = usuario
        self.root.destroy()

    def executar(self):
        self.root.mainloop()
        return self.usuario_logado
