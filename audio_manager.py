import threading
import sounddevice as sd
import numpy as np

class AudioManager:
    def __init__(self):
        self.gravacao = None
        self.gravando = False
        self.fs = 48000
        self.canais = 1
        
        # Usa Windows DirectSound (5 = Mic Realtek, 7 = Speaker Realtek)
        try:
            sd.default.device = (5, 7)
        except Exception as e:
            print(f'Aviso: usando dispositivo padrao ({e})')

        print(f'Configurado: DirectSound {self.fs}Hz ({self.canais}ch)')

    def iniciar_gravacao(self, duracao=5, callback_fim=None):
        if self.gravando:
            return
        self.gravando = True
        thread = threading.Thread(
            target=self._gravar_thread,
            args=(duracao, callback_fim),
            daemon=True
        )
        thread.start()

    def _gravar_thread(self, duracao, callback_fim):
        try:
            self.gravacao = sd.rec(
                int(duracao * self.fs),
                samplerate=self.fs,
                channels=self.canais,
                dtype='float32'
            )
            sd.wait()
        except Exception as e:
            print(f'Erro ao gravar: {e}')
            self.gravacao = None
        finally:
            self.gravando = False
            if callback_fim:
                callback_fim()

    def reproduzir(self, callback_fim=None):
        if self.gravacao is None:
            print('Nenhum audio gravado.')
            return
        thread = threading.Thread(
            target=self._reproduzir_thread,
            args=(callback_fim,),
            daemon=True
        )
        thread.start()

    def _reproduzir_thread(self, callback_fim):
        try:
            sd.play(self.gravacao, self.fs)
            sd.wait()
        except Exception as e:
            print(f'Erro ao reproduzir: {e}')
        finally:
            if callback_fim:
                callback_fim()
