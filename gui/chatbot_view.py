import customtkinter as ctk

from services.chatbot_service import (
    ChatbotService
)


class ChatbotView:

    def __init__(
        self,
        parent
    ):

        self.frame = ctk.CTkFrame(
            parent
        )

        titulo = ctk.CTkLabel(
            self.frame,
            text="Assistente IA"
        )

        titulo.pack(
            pady=5
        )

        self.pergunta = ctk.CTkEntry(
            self.frame,
            width=500,
            placeholder_text="Digite sua pergunta"
        )

        self.pergunta.pack(
            pady=5
        )

        btn = ctk.CTkButton(
            self.frame,
            text="Perguntar",
            command=self.perguntar
        )

        btn.pack(
            pady=5
        )

        self.resposta = ctk.CTkTextbox(
            self.frame,
            width=700,
            height=120
        )

        self.resposta.pack(
            pady=5
        )

    def perguntar(self):

        texto = self.pergunta.get()

        resposta = (
            ChatbotService.responder(
                2,
                texto
            )
        )

        self.resposta.delete(
            "0.0",
            "end"
        )

        self.resposta.insert(
            "0.0",
            resposta
        )