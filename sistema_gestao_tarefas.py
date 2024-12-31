import os
from pathlib import Path
import utilizador

# Classe SistemaGestaoTarefas que manipula utilizadores
class SistemaGestaoTarefas():
    # Inicializacia a classe
    def __init__(self):
        self.__lista_users = []
        # Verifica a existência de um caminho, cria um caso não exista
        if not os.path.isdir(Path("users")):
            os.mkdir("users")
        self.listar_users()

    # Função para listar utilizadores a partir de um ficheiro
    def listar_users(self):
        if os.path.isfile(Path("users/users.txt")):
            with open(Path("users/users.txt"), "r") as file:
                for l in file:
                    line = l.strip()
                    # Caso a linha não seja vazia, carregar utilizador
                    if line != "":
                        cred = line.split(":", 1)
                        self.__lista_users.append(utilizador.Utilizador(cred[0], cred[1]))

    # Função para verificar se um utilizador existe e retorna a sua posição na lista de utilizadores
    def check_user(self, uname):
        n = 0
        for user in self.__lista_users:
            if user.get_uname() == uname:
                return n
            n += 1
        return None

    # Função para autenticação de utilizador
    def auth(self, uname, passwd):
        x = self.check_user(uname)
        if x is not None:
            if self.__lista_users[x].auth(uname, passwd):
                return self.__lista_users[x]
        return False

    # Função para adicionar utilizador
    def add_user(self, uname, passwd):
        # Criação de novo utilizador e armazenamento no ficheiro
        self.__lista_users.append(utilizador.Utilizador(uname, passwd, create=True))

    # Função para alterar a password
    def change_passwd(self, oldpasswd, newpasswd, uname):
        n = 0
        i = self.check_user(uname)
        if self.auth(uname, oldpasswd): # Verificar se é para alterar
            # Guardar o ficheiro antigo numa lista
            with open(Path("users/users.txt"), "r") as file:
                lines = file.readlines()
            with open(Path("users/users.txt"), "w") as file:
                for line in lines:
                    if n == i:
                        # Não escrever a linha que tem o utilizador que vai ser alterado
                        continue
                    file.write(line)
                    n = n + 1
            # Retirar o utilizador alterado da lista
            self.__lista_users.pop(i)
            # Adicionar o utilizador outra vez com as alterações
            self.add_user(uname, newpasswd)
            return True
        else:
            return False
