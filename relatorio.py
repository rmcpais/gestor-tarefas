from pathlib import Path
import os

# Classe Relatório com método para gerar o relatório
class Relatorio:
    # Inicializa a Classe
    def __init__(self):
        # Verifica se há caminho e cria caso não exista
        if not os.path.isdir(Path("relatorios")):
            os.mkdir("relatorios")

    # Função para gerar relatório e guardar num ficheiro a partir de uma lista de tarefas
    def gerar_relatorio(self, lista_tarefas, caminho):
        with open(Path(f"relatorios/{caminho}"), "w") as file:
            for tarefa in lista_tarefas:
                file.write(str(tarefa) + "\n")
