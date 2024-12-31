from pathlib import Path
import os
import hashlib

class Utilizador():
    def __init__(self, uname, passwd, create=False):
        self.__uname = uname
        if create:
            self.__salt = os.urandom(32)
            self.__passwd = self.hash_passwd(passwd)
            with open(Path("users/users.txt"), "a") as file:
                file.write(f"{self.__uname}:{self.__passwd.hex()} {self.__salt.hex()}\n")
        else:
            cred = passwd.split(" ")
            self.__passwd = bytes.fromhex(cred[0])
            self.__salt = bytes.fromhex(cred[1])

    def hash_passwd(self, passwd):
        return hashlib.pbkdf2_hmac('sha256', passwd.encode('utf-8'), self.__salt, 100000)

    def get_uname(self):
        return self.__uname

    def auth(self, uname, passwd):
        if uname == self.__uname and self.hash_passwd(passwd) == self.__passwd:
            return True
        return False
