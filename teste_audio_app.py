import tkinter as tk
from audio_manager import AudioManager

root = tk.Tk()
root.title('AcolheMind - Teste de Audio')
root.geometry('320x180')

audio = AudioManager()

lbl_status = tk.Label(root, text='Clique em Gravar para testar', font=('Arial', 10))
lbl_status.pack(pady=15)

def fim_gravacao():
    root.after(0, lambda: lbl_status.config(text='Gravacao concluida! Clique em Ouvir.'))

def fim_reproducao():
    root.after(0, lambda: lbl_status.config(text='Reproducao finalizada.'))

def acao_gravar():
    lbl_status.config(text='Gravando por 5 segundos...')
    audio.iniciar_gravacao(duracao=5, callback_fim=fim_gravacao)

def acao_ouvir():
    lbl_status.config(text='Reproduzindo audio...')
    audio.reproduzir(callback_fim=fim_reproducao)

tk.Button(root, text='Gravar (5s)', command=acao_gravar, width=20).pack(pady=5)
tk.Button(root, text='Ouvir Gravacao', command=acao_ouvir, width=20).pack(pady=5)

root.mainloop()
