import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)
from sistema_gestao_tarefas import SistemaGestaoTarefas
from task_window import TaskWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.sistema = SistemaGestaoTarefas()

        self.setWindowTitle("Login")
        self.setGeometry(400, 150, 300, 200)

        self.layout = QFormLayout()

        # Campos de entrada
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Botões
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.handle_login)

        self.create_account_button = QPushButton("Criar Conta", self)
        self.create_account_button.clicked.connect(self.show_create_account_window)

        # Adicionar widgets ao layout
        self.layout.addRow(self.username_label, self.username_input)
        self.layout.addRow(self.password_label, self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.create_account_button)

        self.setLayout(self.layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.sistema.auth(username, password):
            self.accept_login(username)
        else:
            self.show_error("Erro", "Username ou password incorrectos!")

    def show_error(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def accept_login(self, username):
        self.close()
        self.task_window = TaskWindow(username)
        self.task_window.show()

    def show_create_account_window(self):
        self.create_account_window = CreateAccountWindow(self.sistema)
        self.create_account_window.show()

class CreateAccountWindow(QWidget):
    def __init__(self, sistema):
        super().__init__()

        self.sistema = sistema

        self.setWindowTitle("Criar Conta")
        self.setGeometry(400, 150, 300, 200)

        self.layout = QFormLayout()

        # Campos de entrada
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_label = QLabel("Confirmar Password:")
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        # Botão para criar conta
        self.create_account_button = QPushButton("Criar Conta", self)
        self.create_account_button.clicked.connect(self.create_account)

        # Adicionar widgets ao layout
        self.layout.addRow(self.username_label, self.username_input)
        self.layout.addRow(self.password_label, self.password_input)
        self.layout.addRow(self.confirm_password_label, self.confirm_password_input)
        self.layout.addWidget(self.create_account_button)

        self.setLayout(self.layout)

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if password != confirm_password:
            self.show_error("Erro", "As passwords não coincidem!")
        elif self.sistema.check_user(username) is not None:
            self.show_error("Erro", "Username já existe!")
        else:
            self.sistema.add_user(username, password)
            self.show_message("Conta criada", "Conta criada com sucesso!")
            self.close()

    def show_error(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
