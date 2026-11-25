import customtkinter as ctk

from gui.chatbot_view import (
    ChatbotView
)

root = ctk.CTk()

chat = ChatbotView(
    root
)

chat.frame.pack(
    padx=20,
    pady=20
)

root.mainloop()