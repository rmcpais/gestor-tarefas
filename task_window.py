from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QRadioButton, QHBoxLayout
)
from tarefa import Tarefa
from relatorio import Relatorio
from lista_de_tarefas import ListaDeTarefas
from sistema_gestao_tarefas import SistemaGestaoTarefas


class TaskWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        

        self.username = username
        self.relatorios = Relatorio()
        self.lista_tarefas = ListaDeTarefas(username)
        self.setWindowTitle(f"Gestão de Tarefas - {self.username}")
        self.setGeometry(400, 150, 600, 400)

        # Layout principal
        self.layout = QVBoxLayout()

        # Sessão 1: Adicionar e remover tarefas
        self.add_task_button = QPushButton("Adicionar Tarefa", self)
        self.add_task_button.clicked.connect(self.show_add_task_form)

        self.remove_task_button = QPushButton("Remover Tarefa", self)
        self.remove_task_button.clicked.connect(self.remove_task)

        self.layout.addWidget(self.add_task_button)
        self.layout.addWidget(self.remove_task_button)

        # Sessão 2: Filtrar tarefas
        self.filter_layout = QHBoxLayout()

        self.filter_todos_button = QRadioButton("Todos", self)
        self.filter_todos_button.setChecked(True)  # Marcar como padrão para todos

        self.filter_pendente_button = QRadioButton("Pendente", self)
        self.filter_concluida_button = QRadioButton("Concluída", self)

        self.filter_layout.addWidget(self.filter_todos_button)
        self.filter_layout.addWidget(self.filter_pendente_button)
        self.filter_layout.addWidget(self.filter_concluida_button)

        # Centralizando os radio buttons
        self.filter_layout.setAlignment(Qt.AlignCenter)

        self.layout.addLayout(self.filter_layout)

        # Conectar os radio buttons ao método de filtragem
        self.filter_todos_button.toggled.connect(self.filter_tasks)
        self.filter_pendente_button.toggled.connect(self.filter_tasks)
        self.filter_concluida_button.toggled.connect(self.filter_tasks)

        # Sessão 3: Exibir tarefas
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Título", "Categoria", "Status", "Data de Criação"])
        self.task_table.cellDoubleClicked.connect(self.edit_task)  # Detectar duplo clique na célula
        self.layout.addWidget(self.task_table)

        # Sessão 4: Relatório, senha e logout
        self.generate_report_button = QPushButton("Gerar Relatório", self)
        self.generate_report_button.clicked.connect(self.report)
        self.change_password_button = QPushButton("Mudar Senha", self)
        self.change_password_button.clicked.connect(self.change_password)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.logout)

        self.layout.addWidget(self.generate_report_button)
        self.layout.addWidget(self.change_password_button)
        self.layout.addWidget(self.logout_button)

        self.setLayout(self.layout)
        self.update_task_table()

    def change_pass(self):
        form = QFormLayout()
    def show_add_task_form(self):
        # Formulário para adicionar tarefa
        form = QFormLayout()

        self.title_input = QLineEdit(self)
        self.description_input = QTextEdit(self)
        self.category_input = QComboBox(self)
        self.category_input.addItems(["Trabalho", "Pessoal", "Estudos"])
        self.status_input = QComboBox(self)
        self.status_input.addItems(["Pendente", "Concluída"])

        form.addRow("Título:", self.title_input)
        form.addRow("Descrição:", self.description_input)
        form.addRow("Categoria:", self.category_input)
        form.addRow("Status:", self.status_input)

        self.add_task_dialog = QWidget()
        self.add_task_dialog.setWindowTitle("Adicionar Tarefa")
        self.add_task_dialog.setLayout(form)

        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self.add_task)
        form.addRow(save_button)

        self.add_task_dialog.show()

    def add_task(self):
        # Adicionar tarefa à lista
        titulo = self.title_input.text()
        descricao = self.description_input.toPlainText()
        categoria = self.category_input.currentText()
        status = self.status_input.currentText()

        if titulo.strip() == "":
            self.show_error("Erro", "O título não pode estar vazio.")
            return

        nova_tarefa = Tarefa(titulo, descricao, categoria, status)
        self.lista_tarefas.adicionar_tarefa(nova_tarefa)

        self.show_message("Sucesso", "Tarefa adicionada com sucesso!")
        self.update_task_table()
        self.add_task_dialog.close()

    def remove_task(self):
        # Remover a tarefa selecionada
        selected_row = self.task_table.currentRow()
        if selected_row == -1:
            self.show_error("Erro", "Selecione uma tarefa para remover.")
            return

        tarefa_removida = self.lista_tarefas.tarefas.pop(selected_row)
        self.show_message("Sucesso", f"Tarefa '{tarefa_removida.titulo}' removida.")
        self.update_task_table()

    def edit_task(self, row, column):
        # Editar a tarefa selecionada
        if row == -1:
            return
        
        tarefa = self.lista_tarefas.tarefas[row]

        # Janela de edição
        form = QFormLayout()

        self.edit_title_input = QLineEdit(self)
        self.edit_title_input.setText(tarefa.titulo)

        self.edit_description_input = QTextEdit(self)
        self.edit_description_input.setText(tarefa.descricao)

        self.edit_category_input = QComboBox(self)
        self.edit_category_input.addItems(["Trabalho", "Pessoal", "Estudos"])
        self.edit_category_input.setCurrentText(tarefa.categoria)

        self.edit_status_input = QComboBox(self)
        self.edit_status_input.addItems(["Pendente", "Concluída"])
        self.edit_status_input.setCurrentText(tarefa.status)

        form.addRow("Título:", self.edit_title_input)
        form.addRow("Descrição:", self.edit_description_input)
        form.addRow("Categoria:", self.edit_category_input)
        form.addRow("Status:", self.edit_status_input)

        self.edit_task_dialog = QWidget()
        self.edit_task_dialog.setWindowTitle("Editar Tarefa")
        self.edit_task_dialog.setLayout(form)

        save_button = QPushButton("Salvar Alterações")
        save_button.clicked.connect(lambda: self.save_edited_task(tarefa, row))
        form.addRow(save_button)

        self.edit_task_dialog.show()

    def save_edited_task(self, tarefa, row):
        # Salvar as alterações feitas
        tarefa.titulo = self.edit_title_input.text()
        tarefa.descricao = self.edit_description_input.toPlainText()
        tarefa.categoria = self.edit_category_input.currentText()
        tarefa.status = self.edit_status_input.currentText()

        self.show_message("Sucesso", "Tarefa editada com sucesso!")
        self.update_task_table()
        self.edit_task_dialog.close()

    def filter_tasks(self):
        tarefas_filtradas = []

        if self.filter_todos_button.isChecked():
            tarefas_filtradas += self.lista_tarefas.tarefas  # Todas as tarefas
        elif self.filter_pendente_button.isChecked():
            tarefas_filtradas += self.lista_tarefas.filtrar_tarefas(status="Pendente")
        elif self.filter_concluida_button.isChecked():
            tarefas_filtradas += self.lista_tarefas.filtrar_tarefas(status="Concluída")

        self.update_task_table(tarefas_filtradas)

    def report(self):
        self.report_window= CreateRelatorioWindow(self.username, self.lista_tarefas)
        self.report_window.show()

    def change_password(self):
        self.change_password_window= ChangePasswordWindow(self.username)
        self.change_password_window.show()

    def logout(self):
        self.close()

    def update_task_table(self, tarefas=None):
        if tarefas is None:
            tarefas = self.lista_tarefas.tarefas

        self.task_table.setRowCount(len(tarefas))
        for row, tarefa in enumerate(tarefas):
            self.task_table.setItem(row, 0, QTableWidgetItem(tarefa.titulo))
            self.task_table.setItem(row, 1, QTableWidgetItem(tarefa.categoria))
            self.task_table.setItem(row, 2, QTableWidgetItem(tarefa.status))
            self.task_table.setItem(row, 3, QTableWidgetItem(tarefa.data_criacao))

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

class ChangePasswordWindow(QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user
        self.sistema = SistemaGestaoTarefas()

        self.setWindowTitle("Mudar Password")
        self.setGeometry(400, 150, 300, 200)

        self.layout = QFormLayout()

        # Campos de entrada
        self.old_password_label = QLabel("Password Antiga:")
        self.old_password_input = QLineEdit(self)
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_label = QLabel("Confirmar Password:")
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        # Botão para criar conta
        self.create_account_button = QPushButton("Mudar Password", self)
        self.create_account_button.clicked.connect(self.change_password)

        # Adicionar widgets ao layout
        self.layout.addRow(self.old_password_label, self.old_password_input)
        self.layout.addRow(self.password_label, self.password_input)
        self.layout.addRow(self.confirm_password_label, self.confirm_password_input)
        self.layout.addWidget(self.create_account_button)

        self.setLayout(self.layout)

    def change_password(self):
        old_password = self.old_password_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if password != confirm_password:
            self.show_error("Erro", "As passwords não coincidem!")
        elif self.sistema.change_passwd(old_password, password, self.user):
            self.show_message("Nova Password", "Password mudada com sucesso!")
            self.close()
        else:
            self.show_error("Erro", "Password antiga errada!")


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

class CreateRelatorioWindow(QWidget):
    def __init__(self, user, lista_tarefas):
        super().__init__()
        self.lista_tarefas = lista_tarefas
        self.relatorios = Relatorio()
        self.username = user
        self.setWindowTitle("Selecionar Categoria para Relatório")
        self.setGeometry(400, 150, 200, 200)

        self.layout = QFormLayout()
        self.category_select_input = QComboBox(self)
        self.category_select_input.addItems(["Todos", "Trabalho", "Pessoal", "Estudos"])
        self.layout.addRow("Escolha a Categoria:", self.category_select_input)

        save_button = QPushButton("Gerar Relatório")
        save_button.clicked.connect(self.gen_report)
        self.layout.addRow(save_button)

        self.setLayout(self.layout)

    def gen_report(self):
        categoria = self.category_select_input.currentText()

        if categoria == "Todos":
            tarefas_filtradas = self.lista_tarefas.tarefas
        else:
            tarefas_filtradas = self.lista_tarefas.filtrar_tarefas(categoria=categoria)

        caminho = f"{self.username}_relatorio_{categoria}.txt"
        self.relatorios.gerar_relatorio(tarefas_filtradas, caminho)
        self.show_message("Relatório", f"Relatório gerado com sucesso em {caminho}")
    
    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()