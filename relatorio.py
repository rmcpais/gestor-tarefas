from pathlib import Path
import os
class Relatorio:
    def __init__(self):
        if not os.path.isdir(Path("relatorios")):
            os.mkdir("relatorios")

    def gerar_relatorio(self, lista_tarefas, caminho):
        with open(Path(f"relatorios/{caminho}"), "w") as file:
            for tarefa in lista_tarefas:
                file.write(str(tarefa) + "\n")
