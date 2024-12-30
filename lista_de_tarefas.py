import os
from pathlib import Path
import tarefa
class ListaDeTarefas():
    def __init__(self, user):
        self.__user = user
        self.__lista_tarefas = []
        if not os.path.isdir(Path("tarefas")):
            os.mkdir("tarefas")
        self.listar_tarefas()

    def listar_tarefas(self):
        if os.path.isfile(Path(f"tarefas/{self.__user}.txt")):
            with open(Path(f"tarefas/{self.__user}.txt"), "r") as file:
                for l in file:
                        line = l.strip()
                        if line != "":
                            t = line.split("/%/")
                            self.__lista_tarefas.append(tarefa.Tarefa(t[0], t[1], t[2], t[3]))
    
    def guardar_lista(self):
        with open(Path(f"tarefas/{self.__user}.txt"), "w") as file:
            for l in self.__lista_tarefas:
                titulo = l.get_titulo()
                desc = l.get_desc()
                categ = l.get_categ()
                status = l.get_status()
                date = l.get_date()
                file.write(f"{titulo}/%/{desc}/%/{categ}/%/{status}/%/{date}\n")
    
    def add_tarefa(self, titulo, desc, categ):
        self.__lista_tarefas.append(tarefa.Tarefa(titulo, desc, categ))
        self.guardar_lista()
    
    def remover_tarefa(self, pos = -1):
        self.__lista_tarefas.pop(pos)
        self.guardar_lista()