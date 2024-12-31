from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QFormLayout,QLineEdit, QTextEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QRadioButton, QHBoxLayout)

from sistema_gestao_tarefas import SistemaGestaoTarefas
from tarefa import Tarefa
from relatorio import Relatorio
from lista_de_tarefas import ListaDeTarefas

# Classe LoginWindow para a janela de login
class LoginWindow(QWidget):
    # Inicialização da janela
    def __init__(self):
        super().__init__()

        # Instância do sistema de gestão de tarefas
        self.sistema = SistemaGestaoTarefas()
        self.notif = SistemaMsgError()

        # Configurações da janela de login
        self.setWindowTitle("Login")
        self.setGeometry(400, 150, 300, 200)
        self.layout = QFormLayout()

        # Campos de entrada
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Botões de login e criar conta
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

    # Função para lidar com o login
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Verificar se o login é válido
        if self.sistema.auth(username, password):
            self.accept_login(username)
        else:
            self.notif.show_error("Erro", "Username ou password incorrectos!")

    # Função para aceitar o login
    def accept_login(self, username):
        self.close()
        self.task_window = TaskWindow(username)
        self.task_window.show()

    # Função para mostrar a janela de criação de conta
    def show_create_account_window(self):
        self.create_account_window = CreateAccountWindow(self.sistema)
        self.create_account_window.show()

# Classe CreateAccountWindow para a janela de criação de conta
class CreateAccountWindow(QWidget):
    # Inicialização da janela
    def __init__(self, sistema):
        super().__init__()

        # Instância do sistema de gestão de tarefas
        self.sistema = sistema
        self.notif = SistemaMsgError()

        # Configurações da janela
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

    # Função para criar a conta
    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Lógica para criar a conta
        if password != confirm_password:
            self.notif.show_error("Erro", "As passwords não coincidem!")
        elif self.sistema.check_user(username) is not None:
            self.notif.show_error("Erro", "Username já existe!")
        else:
            self.sistema.add_user(username, password)
            self.notif.show_message("Conta criada", "Conta criada com sucesso!")
            self.close()

# Classe TaskWindow para a janela de gestão de tarefas
class TaskWindow(QWidget):
    # Inicialização da janela
    def __init__(self, username):
        super().__init__()
        
        # Instância do sistema de gestão de tarefas
        self.username = username
        self.notif = SistemaMsgError()
        self.lista_tarefas = ListaDeTarefas(username)

        # Configurações da janela
        self.setWindowTitle(f"Gestão de Tarefas - {self.username}")
        self.setGeometry(400, 150, 600, 400)
        self.layout = QVBoxLayout()

        # Botões para manipular tarefas
        self.add_task_button = QPushButton("Adicionar Tarefa", self)
        self.add_task_button.clicked.connect(self.show_add_task_form)
        self.remove_task_button = QPushButton("Remover Tarefa", self)
        self.remove_task_button.clicked.connect(self.remove_task)

        # Adicionar botões ao layout
        self.layout.addWidget(self.add_task_button)
        self.layout.addWidget(self.remove_task_button)
        self.filter_layout = QHBoxLayout()

        # Botões de filtro
        self.filter_todos_button = QRadioButton("Todos", self)
        self.filter_todos_button.setChecked(True)  # Marcar como padrão para todos
        self.filter_pendente_button = QRadioButton("Pendente", self)
        self.filter_concluida_button = QRadioButton("Concluída", self)

        # Adicionar radio buttons ao layout
        self.filter_layout.addWidget(self.filter_todos_button)
        self.filter_layout.addWidget(self.filter_pendente_button)
        self.filter_layout.addWidget(self.filter_concluida_button)
        self.filter_layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.filter_layout)

        # Conectar os radio buttons ao método de filtragem
        self.filter_todos_button.toggled.connect(self.filter_tasks)
        self.filter_pendente_button.toggled.connect(self.filter_tasks)
        self.filter_concluida_button.toggled.connect(self.filter_tasks)

        # Tabela de tarefas
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Título", "Categoria", "Status", "Data de Criação"])
        self.task_table.cellDoubleClicked.connect(self.edit_task)  # Detectar duplo clique na célula
        self.layout.addWidget(self.task_table)

        # Botões para gerar relatório, mudar senha e logout
        self.generate_report_button = QPushButton("Gerar Relatório", self)
        self.generate_report_button.clicked.connect(self.report)
        self.change_password_button = QPushButton("Mudar Senha", self)
        self.change_password_button.clicked.connect(self.change_password)
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.logout)

        # Adicionar botões ao layout
        self.layout.addWidget(self.generate_report_button)
        self.layout.addWidget(self.change_password_button)
        self.layout.addWidget(self.logout_button)
        self.setLayout(self.layout)
        # Atualizar a tabela de tarefas
        self.update_task_table()

    
    # Função para mostrar a janela de adição de tarefa
    def show_add_task_form(self):
        # Formulário para adicionar tarefa
        form = QFormLayout()
        # Campos de entrada
        self.title_input = QLineEdit(self)
        self.description_input = QTextEdit(self)
        self.category_input = QComboBox(self)
        self.category_input.addItems(["Trabalho", "Pessoal", "Estudos"])
        self.status_input = QComboBox(self)
        self.status_input.addItems(["Pendente", "Concluída"])

        # Adicionar campos ao formulário
        form.addRow("Título:", self.title_input)
        form.addRow("Descrição:", self.description_input)
        form.addRow("Categoria:", self.category_input)
        form.addRow("Status:", self.status_input)

        # Janela de diálogo para adicionar tarefa
        self.add_task_dialog = QWidget()
        self.add_task_dialog.setWindowTitle("Adicionar Tarefa")
        self.add_task_dialog.setLayout(form)

        # Botão para salvar a tarefa
        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self.add_task)
        form.addRow(save_button)
        # Mostrar a janela de diálogo
        self.add_task_dialog.show()

    # Função para adicionar tarefa
    def add_task(self):
        # Adicionar a tarefa à lista de tarefas
        titulo = self.title_input.text()
        descricao = self.description_input.toPlainText()
        categoria = self.category_input.currentText()
        status = self.status_input.currentText()

        # Verificar se o título está vazio  
        if titulo.strip() == "":
            self.show_error("Erro", "O título não pode estar vazio.")
            return

        # Criar a nova tarefa
        nova_tarefa = Tarefa(titulo, descricao, categoria, status)
        self.lista_tarefas.adicionar_tarefa(nova_tarefa)

        # Mostrar mensagem de sucesso   
        self.notif.show_message("Sucesso", "Tarefa adicionada com sucesso!")
        # Atualizar a tabela de tarefas
        self.update_task_table()
        # Fechar a janela de diálogo
        self.add_task_dialog.close()

    # Função para remover tarefa
    def remove_task(self):
        # Remover a tarefa selecionada
        selected_row = self.task_table.currentRow()
        # Verificar se uma tarefa foi selecionada
        if selected_row == -1:
            self.notif.show_error("Erro", "Selecione uma tarefa para remover.")
            return
    
        # Remover a tarefa da lista
        tarefa_removida = self.lista_tarefas.remover_tarefa(selected_row)
        # Mostrar mensagem de sucesso
        self.notif.show_message("Sucesso", f"Tarefa '{tarefa_removida.titulo}' removida.")
        # Atualizar a tabela de tarefas
        self.update_task_table()

    # Função para editar tarefa
    def edit_task(self, row):
        # Verificar se uma tarefa foi selecionada corretamente
        if row == -1:
            return
        # Obter a tarefa selecionada
        self.tarefa_edit = self.lista_tarefas.tarefas[row]

        # Janela de edição
        form = QFormLayout()

        # Campos de entrada
        self.edit_title_input = QLineEdit(self)
        self.edit_title_input.setText(self.tarefa_edit.titulo)
        self.edit_description_input = QTextEdit(self)
        self.edit_description_input.setText(self.tarefa_edit.descricao)
        self.edit_category_input = QComboBox(self)
        self.edit_category_input.addItems(["Trabalho", "Pessoal", "Estudos"])
        self.edit_category_input.setCurrentText(self.tarefa_edit.categoria)
        self.edit_status_input = QComboBox(self)
        self.edit_status_input.addItems(["Pendente", "Concluída"])
        self.edit_status_input.setCurrentText(self.tarefa_edit.status)

        # Adicionar campos ao formulário
        form.addRow("Título:", self.edit_title_input)
        form.addRow("Descrição:", self.edit_description_input)
        form.addRow("Categoria:", self.edit_category_input)
        form.addRow("Status:", self.edit_status_input)

        # Janela de diálogo para editar tarefa
        self.edit_task_dialog = QWidget()
        self.edit_task_dialog.setWindowTitle("Editar Tarefa")
        self.edit_task_dialog.setLayout(form)

        # Botão para salvar as alterações
        save_button = QPushButton("Salvar Alterações")
        save_button.clicked.connect(self.save_edited_task)
        form.addRow(save_button)

        # Mostrar a janela de diálogo
        self.edit_task_dialog.show()

    # Função para salvar as alterações feitas
    def save_edited_task(self):
        # Salvar as alterações feitas
        self.tarefa_edit.titulo = self.edit_title_input.text()
        self.tarefa_edit.descricao = self.edit_description_input.toPlainText()
        self.tarefa_edit.categoria = self.edit_category_input.currentText()
        self.tarefa_edit.status = self.edit_status_input.currentText()
        self.lista_tarefas.guardar_lista()

        # Mostrar mensagem de sucesso
        self.notif.show_message("Sucesso", "Tarefa editada com sucesso!")
        self.update_task_table()
        self.edit_task_dialog.close()

    # Função para filtrar tarefas
    def filter_tasks(self):
        # Filtrar tarefas com base no status
        tarefas_filtradas = []

        # Verificar o botão selecionado
        if self.filter_todos_button.isChecked():
            tarefas_filtradas += self.lista_tarefas.tarefas  # Todas as tarefas
        elif self.filter_pendente_button.isChecked():
            tarefas_filtradas += self.lista_tarefas.filtrar_tarefas(status="Pendente")
        elif self.filter_concluida_button.isChecked():
            tarefas_filtradas += self.lista_tarefas.filtrar_tarefas(status="Concluída")

        # Atualizar a tabela de tarefas
        self.update_task_table(tarefas_filtradas)

    # Função para gerar relatório
    def report(self):
        # Mostrar a janela de relatório
        self.report_window= CreateRelatorioWindow(self.username, self.lista_tarefas)
        self.report_window.show()

    # Função para mudar a password
    def change_password(self):
        # Mostrar a janela de mudar password
        self.change_password_window= ChangePasswordWindow(self.username)
        self.change_password_window.show()

    # Função para fazer logout
    def logout(self):
        # Fechar a janela de tarefas
        self.close()

    # Função para atualizar a tabela de tarefas
    def update_task_table(self, tarefas=None):
        # Limpar a tabela
        if tarefas is None:
            tarefas = self.lista_tarefas.tarefas
        
        # Limpar a tabela
        self.task_table.setRowCount(len(tarefas))
        for row, tarefa in enumerate(tarefas):
            self.task_table.setItem(row, 0, QTableWidgetItem(tarefa.titulo))
            self.task_table.setItem(row, 1, QTableWidgetItem(tarefa.categoria))
            self.task_table.setItem(row, 2, QTableWidgetItem(tarefa.status))
            self.task_table.setItem(row, 3, QTableWidgetItem(tarefa.data_criacao))

# Classe ChangePasswordWindow para a janela de mudar password
class ChangePasswordWindow(QWidget):
    # Inicialização da janela
    def __init__(self, user):
        super().__init__()

        # Instância do sistema de gestão de tarefas
        self.user = user
        self.notif = SistemaMsgError()
        self.sistema = SistemaGestaoTarefas()

        # Configurações da janela  
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

    # Função para mudar a password
    def change_password(self):
        # Mudar a password
        old_password = self.old_password_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Verificar se a password antiga está correta
        if password != confirm_password:
            self.notif.show_error("Erro", "As passwords não coincidem!")
        elif self.sistema.change_passwd(old_password, password, self.user):
            self.notif.show_message("Nova Password", "Password mudada com sucesso!")
            self.close()
        else:
            self.notif.show_error("Erro", "Password antiga errada!")

# Classe CreateRelatorioWindow para a janela de criar relatório
class CreateRelatorioWindow(QWidget):
    # Inicialização da janela
    def __init__(self, user, lista_tarefas):
        super().__init__()

        # Instância do sistema de gestão de tarefas
        self.lista_tarefas = lista_tarefas
        self.notif = SistemaMsgError()
        self.relatorios = Relatorio()
        self.username = user

        # Configurações da janela
        self.setWindowTitle("Selecionar Categoria para Relatório")
        self.setGeometry(400, 150, 200, 100)
        self.layout = QFormLayout()

        # Selecionar categoria
        self.category_select_input = QComboBox(self)
        self.category_select_input.addItems(["Todos", "Trabalho", "Pessoal", "Estudos"])

        # Botão para gerar relatório
        save_button = QPushButton("Gerar Relatório")
        save_button.clicked.connect(self.gen_report)

        # Adicionar widgets ao layout
        self.layout.addRow("Escolha a Categoria:", self.category_select_input)
        self.layout.addRow(save_button)
        self.setLayout(self.layout)

    # Função para gerar relatório
    def gen_report(self):
        # Gerar o relatório
        categoria = self.category_select_input.currentText()

        # Filtrar tarefas com base na categoria
        if categoria == "Todos":
            tarefas_filtradas = self.lista_tarefas.tarefas
        else:
            tarefas_filtradas = self.lista_tarefas.filtrar_tarefas(categoria=categoria)

        # Gerar o relatório
        caminho = f"{self.username}_relatorio_{categoria}.txt"
        self.relatorios.gerar_relatorio(tarefas_filtradas, caminho)
        self.notif.show_message("Relatório", f"Relatório gerado com sucesso em {caminho}")
        self.close()

# Classe SistemaMsgError para mostrar mensagens de erro
class SistemaMsgError():
    # Inicialização da janela
    def __init__(self):
        pass

    # Função para mostrar mensagem de erro
    def show_error(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    # Função para mostrar mensagem de sucesso
    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()