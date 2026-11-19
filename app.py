from gui.main_window import MainWindow
from database.connection import criar_banco

criar_banco()

app = MainWindow()

app.executar()