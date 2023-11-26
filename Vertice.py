class Vertice:
    def __init__(self, numero_vertice,nivel_pai,numero_pai = None):
        self.marcado = False
        self.adjacencia = list()
        self.numero = numero_vertice
        self.nivel_na_arvore = nivel_pai
        self.numero_pai = numero_pai

