#Classe Utilizador que guarda todas os métodos e informações do utilizador
class Utilizador():
    #inicializar a classe
    def __init__(self, user, passwd):
        self.__user = user
        self.__passwd = passwd

    #mudar a password
    def change_passwd(self, oldpwd, newpwd):
        if oldpwd == self.__passwd:
            self.__passwd = newpwd
    
    def change_user(self, newusr):
        self.__user = newusr

    def get_user(self):
        return self.__user

    def auth(self, user, passwd):
        if user == self.__user and passwd == self.__passwd:
            return True
        else:
            return False
    
