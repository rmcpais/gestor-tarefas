import datetime

# Classe Tarefa com respetivos atributos
class Tarefa:
    def __init__(self, titulo, descricao, categoria, status="Pendente", data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        self.titulo = titulo
        self.descricao = descricao
        self.data_criacao = data
        self.status = status
        self.categoria = categoria

    def atualizar_status(self, novo_status):
        self.status = novo_status

    def alterar_categoria(self, nova_categoria):
        self.categoria = nova_categoria

    def __str__(self):
        return f"{self.titulo} | {self.categoria} | {self.status} | {self.data_criacao}\nDescrição: {self.descricao}\n"
