import os
from pathlib import Path
import utilizador
class SistemaGestaoTarefas():
    #inicializar a classe
    def __init__(self):
        self.__lista_users = []
        #criar a diretoria que vai ter o ficheiro dos utilizadores
        if not os.path.isdir(Path("users")):
            os.mkdir("users")
        self.listar_users()
    
    #guardar os utilizadores todos numa lista
    def listar_users(self):
        if os.path.isfile(Path("users/users.txt")):
            with open(Path("users/users.txt"), "r") as file:
                for l in file:
                    line = l.strip()
                    if line != "":
                        cred = line.split(":", 1)
                        self.__lista_users.append(utilizador.Utilizador(cred[0], cred[1]))
    
    #função que verifica a existencia de um utilizador e retorna o index deste na lista de utilizadores
    def check_user(self, uname):
        n = 0
        for user in self.__lista_users:
            if user.get_uname() == uname:
                return n
            n = n + 1
        return None

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

        
    #função para adicionar utilizadores
    def add_user(self, uname, passwd):
        if self.check_user(uname) is None: #verificar se o utilizador existe
            #adicionar o novo utilizador
            self.__lista_users.append(utilizador.Utilizador(uname, passwd, True))
            return
        
    #função para autenticar o utilizador
    def auth(self, uname, passwd):
        x = self.check_user(uname)
        if x != None: #verificar se o utilizador não existe
            if self.__lista_users[x].auth(uname, passwd): #autenticar o utilizador
                return self.__lista_users[x] #retornar o utilizador
        return False
