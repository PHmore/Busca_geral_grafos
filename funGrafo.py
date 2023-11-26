# Aqui estarão as outras funções

# Apresentar o grafo visualmente acima da opções

# Verificar se é conexo

'''
Será retornado 1 caso seja conexo e será retornado NULL caso não seja
Caso o usuário selecione a opção “1” o programa deve responder SIM, caso o grafo seja conexo,
ou NÃO, caso o grafo seja desconexo. Na sequência devem ser apresentados os conjuntos
correspondentes a cada componente conexa que o grafo possuir
'''




# Exibir o grau de cada vértice


# Aplicar busca em largura


# Encontrar bipartição
"""
class Vertice:
    def __init__(self, numero, adjacencia):
        self.numero = numero
        self.adjacencia = adjacencia

def verifica_bipartido(vertices):
    groupA = set()
    groupB = set()

    for v in vertices:
        if v not in groupA and v not in groupB:
            groupA.add(v)
            stack = [v]

            while stack:
                current = stack.pop()

                for adj in vertices[current].adjacencia:
                    if adj in groupA:
                        return False  # Se um vértice adjacente já está em groupA, o grafo não é bipartido
                    elif adj not in groupB:
                        groupB.add(adj)
                        stack.append(adj)

    return True  # Se nenhum conflito for encontrado, o grafo é bipartido

# Exemplo de uso:
vertices = {
    1: Vertice(1, [2, 3]),
    2: Vertice(2, [1, 4]),
    3: Vertice(3, [1, 4]),
    4: Vertice(4, [2, 3])
}

resultado = verifica_bipartido(vertices)
if resultado:
    print("O grafo é bipartido.")
else:
    print("O grafo não é bipartido.")

"""

"""
7 – Caso o grafo seja bipartido, a opção 3 deve apresentar a bipartição do grafo, caso ele não seja
bipartido, esta opção deve informar que é impossível encontrar a bipartição porque o grafo não é
bipartido, em seguida apresentar o ciclo ímpar que há no grafo
"""

# !A implementação deve ser original, i.e. não usar bibliotecas prontas para efetuar as principais
# !tarefas solicitadas;


"""
ALTERNATIVA de leitura dos vértices usando matriz de adjacência

def calcular_grau_vertice(matriz_adjacencia):
    graus = []
    num_vertices = len(matriz_adjacencia)

    for i in range(num_vertices):
        grau = 0
        for j in range(num_vertices):
            if matriz_adjacencia[i][j] == 1:
                grau += 1
        graus.append(grau)
    print(graus)
    return graus

# Exemplo de uso
matriz_adjacencia = [
    [0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 1, 1, 0]
]

graus = calcular_grau_vertice(matriz_adjacencia)

for i, grau in enumerate(graus):
    print(f"O vértice {i+1} tem grau {grau}.")

    


def dfs(grafo, vertice, visitados):
    visitados.add(vertice)
    for vizinho in grafo[vertice]:
        if vizinho not in visitados:
            dfs(grafo, vizinho, visitados)

def grafo_desconexo(grafo):
    visitados = set()
    componente = 0

    for vertice in grafo:
        if vertice not in visitados:
            componente += 1
            dfs(grafo, vertice, visitados)

    return componente > 1

# Exemplo de representação de um grafo como dicionário de adjacências
grafo_exemplo = {
    1: [2, 3],
    2: [1],
    3: [1],
    4: [5],
    5: [4]
}

if grafo_desconexo(grafo_exemplo):
    print("O grafo é desconexo.")
else:
    print("O grafo é conexo.")

"""
#! Verifica se é desconexo por meio da busca em profundidade
"""
def dfs(grafo, vertice, visitados):
    visitados.add(vertice)
    for vizinho in grafo[vertice]:
        if vizinho not in visitados:
            dfs(grafo, vizinho, visitados)

def grafo_desconexo(grafo):
    visitados = set()
    componente = 0

    for vertice in grafo:
        if vertice not in visitados:
            componente += 1
            dfs(grafo, vertice, visitados)

    return componente > 1

# Exemplo de representação de um grafo como lista de adjacência
grafo_exemplo = {
    1: [2, 3],
    2: [1],
    3: [1],
    4: [5],
    5: [4]
}

if grafo_desconexo(grafo_exemplo):
    print("O grafo é desconexo.")
else:
    print("O grafo é conexo.")

"""