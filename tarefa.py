from datetime import datetime
class Tarefa():
    def __init__(self, titulo, desc, categ, status = "pendente", date = datetime.now().strftime('%Y-%m-%d')):
        self.__titulo = titulo
        self.__desc = desc
        self.__status = status
        self.__categ = categ
        self.__date = date
    

    def change_status(self):
        if self.__status == "pendente":
            self.__status = "concluída"
        else:
            self.__status = "pendente"

    def get_date(self):
        return self.__date
    
    def get_status(self):
        return self.__status

    def get_titulo(self):
        return self.__titulo
    
    def get_desc(self):
        return self.__desc
    
    def get_categ(self):
        return self.__categ

    def set_categ(self, newcateg):
        self.__categ = newcateg

    def set_desc(self, newdesc):
        self.__desc = newdesc

    def set_titulo(self, newtitulo):
        self.__titulo = newtitulo
