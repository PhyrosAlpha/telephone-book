import json
import os.path
import os


class EscritaJson:
    def __init__(self, dir):
        self.titulo = None
        self.dir = dir
        #self.titulo_arquivo = self.titulo + ".json"
        self.arquivo_escrito = []

    def escrever_json(self):
      #  with open(self.titulo_arquivo, "w") as arquivo:
       #     json.dump(self.arquivo_escrito, arquivo)
        pass

    def atualizar(self):
        with open(self.dir, "w") as arquivo:
            json.dump(self.arquivo_escrito, arquivo)

    def alterar_nova_lista(self):
        with open(self.dir, "w") as arquivo:
            json.dump(self.arquivo_escrito, arquivo)


class LeituraJson:
    def __init__(self, dir):
        self.dir = dir
        self.arquivo_lido = []

    def ler_json(self):
        with open(self.dir) as arquivo:
            self.arquivo_lido = json.load(arquivo)
        arquivo.close()


class CriarDiretorio:
    def __init__(self, nome):
        self.nome = nome

    def criar_diretorio(self):
        try:
            os.mkdir(self.nome)
            return True

        except FileExistsError:
            return False

