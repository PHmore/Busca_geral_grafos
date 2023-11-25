class Vertice:
    def __init__(self, numero_vertice):
        self.marcado = False
        self.adjacencia = list()
        self.numero = numero_vertice
        self.nivel_na_arvore = 0

