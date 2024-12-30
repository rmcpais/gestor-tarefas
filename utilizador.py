#Classe Utilizador que guarda todas os métodos e informações do utilizador
from pathlib import Path
import os
import hashlib
class Utilizador():
    #inicializar a classe
    def __init__(self, uname, passwd, create = False):
        self.__uname = uname
        if create:
            self.__salt = os.urandom(32) #criar um salt para a password
            self.__passwd = self.hash_passwd(passwd)
            with open(Path("users/users.txt"), "a") as file:
                file.write(f"{self.__uname}:{self.__passwd.hex()} {self.__salt.hex()}\n") #guardar o novo utilizador no ficheiro
        else:
            #carregar os dados do ficehiro dos utilizadores
            cred = passwd.split(" ")
            self.__passwd = bytes.fromhex(cred[0])
            self.__salt = bytes.fromhex(cred[1])
            
    #função para dar hash a uma password salted, para guardar/autenticar
    def hash_passwd(self, passwd):
        password = hashlib.pbkdf2_hmac('sha256', passwd.encode('utf-8'), self.__salt, 100000)
        return password
    
    #função getter para o nome de utilizador
    def get_uname(self):
        return self.__uname

    #função de autenticação do utilizador
    def auth(self, uname, passwd):
        if uname == self.__uname and self.hash_passwd(passwd) == self.__passwd:
            return True
        else:
            return False
        