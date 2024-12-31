import os
from tarefa import Tarefa
from pathlib import Path
class ListaDeTarefas:
    
    def __init__(self, user):
        self.tarefas = []
        self.__user = user
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
                            tarefa = Tarefa(t[0], t[1], t[2], t[3], t[4])
                            self.adicionar_tarefa(tarefa)

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)
        self.guardar_lista()

    def remover_tarefa(self, titulo):
        n = 0
        for t in self.tarefas:
            if t.titulo == titulo:
                break
            n = n + 1
        if n != None:
            self.tarefas.pop(n)
            self.guardar_lista()

    def guardar_lista(self):
        with open(Path(f"tarefas/{self.__user}.txt"), "w") as file:
            for t in self.tarefas:
                file.write(f"{t.titulo}/%/{t.descricao}/%/{t.categoria}/%/{t.status}/%/{t.data_criacao}\n")


    def atualizar_tarefa(self, titulo, novos_dados):
        for tarefa in self.tarefas:
            if tarefa.titulo == titulo:
                tarefa.titulo = novos_dados.get("titulo", tarefa.titulo)
                tarefa.descricao = novos_dados.get("descricao", tarefa.descricao)
                tarefa.status = novos_dados.get("status", tarefa.status)
                tarefa.categoria = novos_dados.get("categoria", tarefa.categoria)
                self.guardar_lista()

    def filtrar_tarefas(self, status=None, categoria = None):
        if status or categoria:
            n = 0
            tarefas_filtradas = self.tarefas.copy()
            for t in self.tarefas:
                print(t)
                if t.status == status or t.categoria == categoria:
                    n = n + 1
                    continue
                tarefas_filtradas.pop(n)
                
            return tarefas_filtradas
        
        return self.tarefas

    def __str__(self):
        return "\n".join([str(t) for t in self.tarefas])
 