from pathlib import Path
import os
import hashlib

# Classe Utilizador para gerar e criptografar palavra-passe
class Utilizador():
    # Inicializa a Classe
    def __init__(self, uname, passwd, create=False):
        self.__uname = uname
        if create:
            self.__salt = os.urandom(32)
            self.__passwd = self.hash_passwd(passwd)
            # Guardar nome de utilizador e palavra-passe criptografada em hexadecimal num ficheiro
            with open(Path("users/users.txt"), "a") as file:
                file.write(f"{self.__uname}:{self.__passwd.hex()} {self.__salt.hex()}\n")
        else:
            cred = passwd.split(" ")
            self.__passwd = bytes.fromhex(cred[0])
            self.__salt = bytes.fromhex(cred[1])

    # Função para criptografar a palavra-passe com salt
    def hash_passwd(self, passwd):
        return hashlib.pbkdf2_hmac('sha256', passwd.encode('utf-8'), self.__salt, 100000)

    # Função para retornar username
    def get_uname(self):
        return self.__uname

    # Função de autenticação
    def auth(self, uname, passwd):
        if uname == self.__uname and self.hash_passwd(passwd) == self.__passwd:
            return True
        return False
