import os
from pathlib import Path
import utilizador

class SistemaGestaoTarefas():
    def __init__(self):
        self.__lista_users = []
        if not os.path.isdir(Path("users")):
            os.mkdir("users")
        self.listar_users()

    def listar_users(self):
        if os.path.isfile(Path("users/users.txt")):
            with open(Path("users/users.txt"), "r") as file:
                for l in file:
                    line = l.strip()
                    if line != "":
                        cred = line.split(":", 1)
                        self.__lista_users.append(utilizador.Utilizador(cred[0], cred[1]))

    def check_user(self, uname):
        n = 0
        for user in self.__lista_users:
            if user.get_uname() == uname:
                return n
            n += 1
        return None

    def auth(self, uname, passwd):
        x = self.check_user(uname)
        if x is not None:
            if self.__lista_users[x].auth(uname, passwd):
                return self.__lista_users[x]
        return False

    def add_user(self, uname, passwd):
        # Criação de novo utilizador e armazenamento no ficheiro
        self.__lista_users.append(utilizador.Utilizador(uname, passwd, create=True))

    #função para alterar a password
    def change_passwd(self, oldpasswd, newpasswd, uname):
        n = 0
        i = self.check_user(uname)
        if self.auth(uname, oldpasswd): #verificar se é para alterar
            #guardar o ficheiro antigo numa lista
            with open(Path("users/users.txt"), "r") as file:
                lines = file.readlines()
            with open(Path("users/users.txt"), "w") as file:
                for line in lines:
                    if n == i:
                        #não escrever a linha que tem o utilizador que vai ser alterado
                        continue
                    file.write(line)
                    n = n + 1
            #retirar o utilizador alterado da lista
            self.__lista_users.pop(i)
            #adicionar o utilizador outra vez com as alterações
            self.add_user(uname, newpasswd)
            return True
            #função para alterar a password
    def change_passwd(self, oldpasswd, newpasswd, uname):
        n = 0
        i = self.check_user(uname)
        if self.auth(uname, oldpasswd): #verificar se é para alterar
            #guardar o ficheiro antigo numa lista
            with open(Path("users/users.txt"), "r") as file:
                lines = file.readlines()
            with open(Path("users/users.txt"), "w") as file:
                for line in lines:
                    if n == i:
                        #não escrever a linha que tem o utilizador que vai ser alterado
                        continue
                    file.write(line)
                    n = n + 1
            #retirar o utilizador alterado da lista
            self.__lista_users.pop(i)
            #adicionar o utilizador outra vez com as alterações
            self.add_user(uname, newpasswd)
            return True
        else:
            return False
