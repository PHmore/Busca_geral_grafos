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

    for v in vertices:
        print(v.numero, "Adjacencia",v.adjacencia)
        #Será feito uma coloração onde o vértices e seus adjacentes receberão a mesma cor
        #Dps será conferido quais vértices não foram coloridos e serão colocados de outra cor eles e seu adjacentes

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
            G_connect(G_pgv)

        if event == 'Sair':
            break

    # Fechar a janela
    window.close()

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