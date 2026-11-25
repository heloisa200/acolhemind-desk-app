from tkinter import ttk

import customtkinter as ctk

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


def criar_switch_tema(master, ao_alternar=None):
    """Cria o interruptor "Modo escuro" já na posição certa para o tema atual.

    ao_alternar: função opcional chamada depois da troca (ex.: recolorir tabela).
    """
    switch = ctk.CTkSwitch(master, text="Modo escuro")

    def alternar():
        ctk.set_appearance_mode("dark" if switch.get() == 1 else "light")
        if ao_alternar:
            ao_alternar()

    switch.configure(command=alternar)
    if ctk.get_appearance_mode() == "Dark":
        switch.select()
    return switch


def aplicar_estilo_tabela():
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
