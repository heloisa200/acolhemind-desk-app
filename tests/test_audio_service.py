import sys
import tempfile
import types
import unittest
from array import array
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from services import audio_service


class AudioServiceTests(unittest.TestCase):
    def test_rejects_duration_outside_supported_range(self):
        for duration in (0, audio_service.MAX_RECORDING_SECONDS + 1):
            with self.subTest(duration=duration):
                with patch.object(audio_service, "_obter_modelo") as obter_modelo:
                    with self.assertRaises(audio_service.AudioServiceError):
                        audio_service.gravar_e_transcrever(duration)
                obter_modelo.assert_not_called()

    def test_records_and_returns_local_transcription(self):
        sounddevice = types.ModuleType("sounddevice")
        sounddevice.rec = lambda *args, **kwargs: array("h", [0, 0])
        sounddevice.wait = lambda: None

        vosk = types.ModuleType("vosk")
        vosk.SetLogLevel = lambda level: None
        vosk.Model = lambda path: object()

        class FakeRecognizer:
            def __init__(self, model, sample_rate):
                self.frames = []

            def AcceptWaveform(self, frame):
                self.frames.append(frame)

            def FinalResult(self):
                return '{"text": "estou sentindo ansiedade"}'

        vosk.KaldiRecognizer = FakeRecognizer

        with (
            patch.dict(sys.modules, {"sounddevice": sounddevice, "vosk": vosk}),
            patch.object(audio_service, "_obter_modelo", return_value=Path("modelo")),
        ):
            resultado = audio_service.gravar_e_transcrever(2)

        self.assertEqual(resultado, "estou sentindo ansiedade")

    def test_rejects_zip_paths_that_escape_extraction_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            archive = Path(temporary_directory) / "modelo.zip"
            with ZipFile(archive, "w") as pacote:
                pacote.writestr("../arquivo-fora.txt", "conteúdo")

            with self.assertRaises(audio_service.AudioServiceError):
                audio_service._extrair_modelo(
                    archive, Path(temporary_directory) / "extraido"
                )


    def test_accepts_flat_layout_of_vosk_small_portuguese_model(self):
        # vosk-model-small-pt-0.3: arquivos soltos na raiz + pasta ivector
        with tempfile.TemporaryDirectory() as temporary_directory:
            modelo = Path(temporary_directory)
            (modelo / "ivector").mkdir()
            (modelo / "final.mdl").write_bytes(b"")
            self.assertTrue(audio_service._modelo_valido(modelo))

    def test_accepts_standard_layout_with_am_and_conf(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            modelo = Path(temporary_directory)
            (modelo / "am").mkdir()
            (modelo / "conf").mkdir()
            self.assertTrue(audio_service._modelo_valido(modelo))

    def test_rejects_incomplete_model_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            self.assertFalse(audio_service._modelo_valido(Path(temporary_directory)))

    def test_downloads_and_installs_flat_layout_model(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            pacote_falso = base / "origem.zip"
            nome = audio_service.MODEL_NAME
            with ZipFile(pacote_falso, "w") as pacote:
                pacote.writestr(f"{nome}/final.mdl", "x")
                pacote.writestr(f"{nome}/Gr.fst", "x")
                pacote.writestr(f"{nome}/HCLr.fst", "x")
                pacote.writestr(f"{nome}/mfcc.conf", "x")
                pacote.writestr(f"{nome}/ivector/final.ie", "x")

            def baixar_falso(arquivo, progresso):
                arquivo.write_bytes(pacote_falso.read_bytes())

            modelos = base / "models"
            with (
                patch.object(audio_service, "_diretorio_modelos", return_value=modelos),
                patch.object(audio_service, "_baixar_modelo", baixar_falso),
            ):
                caminho = audio_service._obter_modelo()

            self.assertEqual(caminho, modelos / nome)
            self.assertTrue((caminho / "final.mdl").is_file())


if __name__ == "__main__":
    unittest.main()
