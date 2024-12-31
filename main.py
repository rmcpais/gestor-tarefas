import sys

from PyQt5.QtWidgets import QApplication
from interface import LoginWindow

# Função para iniciar a janela de Login
def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    # Handle saída
    sys.exit(app.exec_())

main()
