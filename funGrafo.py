# Aqui estarão as outras funções

# Apresentar o grafo visualmente acima da opções

# Verificar se é conexo

'''
Será retornado 1 caso seja conexo e será retornado NULL caso não seja
Caso o usuário selecione a opção “1” o programa deve responder SIM, caso o grafo seja conexo,
ou NÃO, caso o grafo seja desconexo. Na sequência devem ser apresentados os conjuntos
correspondentes a cada componente conexa que o grafo possuir
'''


# Será calculado o grau para que os 3 de maior grau sejam candidatos a raiz
def calcular_grau(grafo):
    grau = {}

    for vertice, vizinhos in grafo.items():
        grau[vertice] = len(vizinhos)

    return grau


# Exemplo de um grafo representado por lista de adjacência
grafo_exemplo = {
    'A': ['B', 'C'],
    'B': ['A', 'C'],
    'C': ['A', 'B', 'D'],
    'D': ['C']
}

graus = calcular_grau(grafo_exemplo)

# Exibir o grau de cada vértice
for vertice, grau in graus.items():
    print(f'O vértice {vertice} possui grau {grau}')

# Aplicar busca em largura


# Encontrar bipartição
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



"""
