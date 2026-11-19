import customtkinter as ctk

class MainWindow:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.title(
            "AcolheMind"
        )

        self.root.geometry(
            "800x600"
        )

        titulo = ctk.CTkLabel(
            self.root,
            text="AcolheMind"
        )

        titulo.pack(
            pady=20
        )

    def executar(self):

        self.root.mainloop()