import PySimpleGUI as sg
from lerGrafo import interface_lerGrafo
from buscaLarg import criar_grafo
from Vertice import Vertice
#from buscaLarg import interface_buscaLarg

# Aqui estarão as outras funções

# Apresentar o grafo visualmente acima da opções

# Verificar se é conexo

def G_connect (G_pgv):
    print("Será feita uma verificação usando busca profunda")
    num_vertices = list()
    vertices = list()
    arestas = []

    arestas = list(G_pgv.edges())
    #Converte uma lista de strings para uma lista de inteiros
    arestas = [(int(aresta[0]), int(aresta[1])) for aresta in arestas ]

    #list_vert = G_pvg.nodes()

    for v in range(len(G_pgv.nodes())):
        novo_no = Vertice(v,-1)
        num_vertices.append(v)
        vertices.append(novo_no)

    for v in vertices:
        for n in arestas:
            if v.numero in n:
                if n[0] == v.numero and n[1] not in v.adjacencia:
                    v.adjacencia.append(n[1])
                    print(v.adjacencia)
                elif n[1] == v.numero and n[0] not in v.adjacencia:
                    v.adjacencia.append(n[0])
                    print(v.adjacencia)

    #Modificar lógica para que guarde cada componente criada por um vértice
    # e suas adjacencias em um vetor que ficará na matriz componentes
    componentes = []
    groupA = list()
    groupB = list()

    for componente in componentes:
        for v in vertices:
            if v.numero not in componente:
                componente.append(v.numero)
                stack = [v.numero]

                while stack:
                    current = stack.pop()

                    for adj in vertices[current].adjacencia:
                        if adj not in componente:
                            # Adiciona aos grupos alternadamente
                            if current in componente:
                                componente.append(adj)
                            else:
                                groupA.append(adj)
                            stack.append(adj)
        
    print("Grupo A : ",groupA,"Grupo B: ",groupB)

def G_bipart (G_pgv):
    num_vertices = list()
    vertices = list()
    arestas = []

    arestas = list(G_pgv.edges())
    #Converte uma lista de strings para uma lista de inteiros
    arestas = [(int(aresta[0]), int(aresta[1])) for aresta in arestas ]

    #list_vert = G_pvg.nodes()

    for v in range(len(G_pgv.nodes())):
        novo_no = Vertice(v,-1)
        num_vertices.append(v)
        vertices.append(novo_no)

    for v in vertices:
        for n in arestas:
            if v.numero in n:
                if n[0] == v.numero and n[1] not in v.adjacencia:
                    v.adjacencia.append(n[1])
                    print(v.adjacencia)
                elif n[1] == v.numero and n[0] not in v.adjacencia:
                    v.adjacencia.append(n[0])
                    print(v.adjacencia)

    #Talvez seja necessário aplicar uma busca em 
    # largura e árvores para mostrar o ciclo impar
    #Está dividindo o grafo se for bipartido
    groupA = list()
    groupB = list()

    print("O grafo é bipartido e a árvore será recolorido em 2 cores diferentes")

    for v in vertices:
        if v.numero not in groupA and v.numero not in groupB:
            groupA.append(v.numero)
            stack = [v.numero]

            while stack:
                current = stack.pop()

                for adj in vertices[current].adjacencia:
                    if adj not in groupA and adj not in groupB:
                        # Adiciona aos grupos alternadamente
                        if current in groupA:
                            groupB.append(adj)
                        else:
                            groupA.append(adj)
                        stack.append(adj)
        
    print("Grupo A : ",groupA,"Grupo B: ",groupB)

#Remover essa interface depois de tiver implementado 
def G_connect_interface (matriz_adjacencia):
    caminho_imagem = "grafo/grafo.png"
    G_pgv = criar_grafo(matriz_adjacencia)
    sg.theme('Reddit')

    # Layout da interface
    layout = [
        [sg.Image(filename=caminho_imagem,key="-IMAGE-")],
        [sg.Push(), sg.Button('Verificar se é conexo',size=(20, 1), button_color=('white', 'DarkGreen'))],
        [sg.Push()],
        [sg.Push(), sg.Button('Sair', size=(20, 1), button_color=('white', 'DarkRed')), sg.Push()]
    ]

    # Criar a janela
    window = sg.Window("Exibir Imagem", layout, resizable=True, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        
        if event == 'Verificar se é conexo':
            print("Será feita " ,event)
            G_bipart(G_pgv)

        if event == 'Sair':
            break

    # Fechar a janela
    window.close()

def bipartGrafo(G_pgv):
    print("Será feita busca em largura")
    num_vertices = list()
    vertices = list()
    arestas = []

    arestas = list(G_pgv.edges())
    #Converte uma lista de strings para uma lista de inteiros
    arestas = [(int(aresta[0]), int(aresta[1])) for aresta in arestas ]

    #list_vert = G_pvg.nodes()

    for v in range(len(G_pgv.nodes())):
        novo_no = Vertice(v,-1)
        num_vertices.append(v)
        vertices.append(novo_no)

    for v in vertices:
        for n in arestas:
            if v.numero in n:
                if n[0] == v.numero and n[1] not in v.adjacencia:
                    v.adjacencia.append(n[1])
                    print(v.adjacencia)
                elif n[1] == v.numero and n[0] not in v.adjacencia:
                    v.adjacencia.append(n[0])
                    print(v.adjacencia)

    #Mini busca em largura para salvar arestas primo e irmã
    fila = []
    fila.append(vertices[0])
    while fila:
        print(fila)
        

matriz = [
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
]

G_connect_interface (matriz)
'''
Será retornado 1 caso seja conexo e será retornado NULL caso não seja
Caso o usuário selecione a opção “1” o programa deve responder SIM, caso o grafo seja conexo,
ou NÃO, caso o grafo seja desconexo. Na sequência devem ser apresentados os conjuntos
correspondentes a cada componente conexa que o grafo possuir
'''


"""
import pygraphviz as pgv

# Suponha que você já tenha um grafo G_pgv

# Função para realizar busca em profundidade (DFS)
def dfs(v, visited, component):
    visited[v] = True
    component.append(v)
    for adj in vertices[v].adjacencia:
        if not visited[adj]:
            dfs(adj, visited, component)

# Verificação de desconexão
def verificar_desconexo(G):
    visited = [False] * len(G.nodes())
    components = []
    
    for v in G.nodes():
        if not visited[v]:
            component = []
            dfs(v, visited, component)
            components.append(component)
    
    return components

# Salvando cada conjunto de vértices e arestas para cada componente
def salvar_componentes_desconexos(components, arestas):
    conjuntos_vertices = []
    conjuntos_arestas = []
    
    for component in components:
        vertices_componente = [vertices[v] for v in component]
        conjuntos_vertices.append(vertices_componente)
        
        arestas_componente = [aresta for aresta in arestas if aresta[0] in component and aresta[1] in component]
        conjuntos_arestas.append(arestas_componente)
    
    return conjuntos_vertices, conjuntos_arestas

# Seu código continua aqui...
# ... (adicionando nós e arestas ao grafo)

# Após adicionar nós e arestas:
vertices = []  # Suponha que você já tenha os vértices definidos
arestas = []   # Suponha que você já tenha as arestas definidas

# Verifica a desconexão
componentes_desconexos = verificar_desconexo(G_pgv)

# Salva os conjuntos de vértices e arestas para cada componente desconexo
conjuntos_vertices, conjuntos_arestas = salvar_componentes_desconexos(componentes_desconexos, arestas)

"""