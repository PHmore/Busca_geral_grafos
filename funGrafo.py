# Importa a biblioteca PySimpleGUI para criar interfaces gráficas e a biblioteca pygraphviz para manipulação de grafos
import PySimpleGUI as sg
import pygraphviz as pgv
from Vertice import Vertice


# Função para calcular o grau de cada vértice no grafo representado pela matriz de adjacência
def calcular_grau_vertice(matriz_adjacencia):
    graus = []
    num_vertices = len(matriz_adjacencia)

    # Calcula o grau de cada vértice somando os elementos da linha correspondente na matriz
    for i in range(num_vertices):
        grau = 0
        for j in range(num_vertices):
            if matriz_adjacencia[i][j] == 1:
                grau += 1
        graus.append(grau)

    # Cria uma tabela com os vértices e seus respectivos graus, ordenada pelo grau decrescente
    dados_tabela = []
    for idx, grau in enumerate(graus):
        dados_tabela.append([f'{idx}', grau])
    dados_tabela.sort(key=lambda x: x[1], reverse=True)

    return dados_tabela


# Função para selecionar um vértice inicial com base nos graus dos vértices
def vert_inicial(grafo):
    # Configuração do tema da interface gráfica
    sg.theme('Reddit')
    dados_tabela = calcular_grau_vertice(grafo)

    # Layout da janela para seleção do vértice inicial
    layout = [
        [sg.Table(values=dados_tabela, headings=['Vértice', 'Grau'], auto_size_columns=True, key='-TABLE-')],
        [sg.Text("Quanto maior o grau mais eficiente a busca", key='-MESSAGE-')],
        [sg.Text('Selecione um item:'), sg.Combo(values=[row[0] for row in dados_tabela], key='-COMBO-')],
        [sg.Button('OK')]
    ]

    # Criação da janela
    window = sg.Window('Interface', layout)

    while True:
        event, values = window.read()

        # Verifica se a janela foi fechada
        if event == sg.WIN_CLOSED:
            return -1

        # Verifica se o botão OK foi pressionado
        if event == 'OK':
            selected_vertex = values['-COMBO-']
            break

    window.close()

    try:
        return int(selected_vertex)
    except:
        return 0


# Função verifica se os vértices encontrados são todos os vértices do grafo
# Se não forem retorna os vértices que não forma encontrados pela busca
def isConnect(vertices_encontrados, vertices_totais, componente=[]):
    vertices_encontrados = set(vertices_encontrados)
    vertices_totais = set(vertices_totais)
    nova_componente = list(vertices_encontrados - set(sum(componente, [])))
    componente.append(nova_componente)
    resultado = vertices_totais - vertices_encontrados

    return list(resultado)


# Função para verificar se um grafo é bipartido e desenhar as partes
def isBipart(vertices, arestas_irmao, arestas_primo, arvore=None, G_pgv=None):
    def draw_bipart(nodes, color, G_pgv=None, arvore=None, arestas=None):
        for node in nodes:
            if G_pgv:
                pgv_node = G_pgv.get_node(node)
                pgv_node.attr['color'] = color
                if arestas:
                    for aresta in arestas:
                        pgv_edge = G_pgv.get_edge(*aresta)
                        pgv_edge.attr['color'] = color
                G_pgv.draw('grafo/grafo.png')
            if arvore:
                pgv_node = arvore.get_node(node)
                pgv_node.attr['color'] = color
                arvore.draw('grafo/arvore.png')

    #Se houver aresta irmão ou primo não é bipartido
    if arestas_irmao or arestas_primo:
        arestas_special = list()
        ciclo_impar_arestas = list()
        ciclo_impar = list()

        if arestas_irmao is not None:
            arestas_special.extend(arestas_irmao)

        if arestas_primo is not None:
            arestas_special.extend(arestas_primo)

        verticeA = None
        verticeB = None

        for v in vertices:
            if v.numero == arestas_special[0][0]:
                verticeA = v

            if v.numero == arestas_special[0][1]:
                verticeB = v

        ciclo_impar_arestas.append(arestas_special[0])
        ciclo_impar.append(verticeA.numero)
        ciclo_impar.append(verticeB.numero)

        # Encontrando um ciclo ímpar na árvore
        while verticeA.numero_pai != verticeB.numero_pai:
            for v in vertices:
                if v.numero == verticeA.numero_pai:
                    ciclo_impar_arestas.append((verticeA.numero, v.numero))
                    verticeA = v
                    break
            for v in vertices:
                if v.numero == verticeB.numero_pai:
                    ciclo_impar_arestas.append((verticeB.numero, v.numero))
                    verticeB = v
                    break
            ciclo_impar.append(verticeA.numero)
            ciclo_impar.append(verticeB.numero)

        ciclo_impar.append(verticeA.numero_pai)
        ciclo_impar_arestas.append((verticeB.numero, verticeA.numero_pai))
        ciclo_impar_arestas.append((verticeA.numero, verticeA.numero_pai))

        # Desenha o ciclo ímpar com cor amarela no grafo
        draw_bipart(ciclo_impar, 'yellow', G_pgv, arvore, ciclo_impar_arestas)

        verticeA = None
        verticeB = None
        print("Ciclo impar: ",ciclo_impar," Arestas do ciclo impar: ",ciclo_impar_arestas)
        ciclo_impar.clear()
        arestas_special.clear()

    else:
        groupA = list()
        groupB = list()

        # Encontrando as partes bipartidas do grafo
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

        # Desenha as partes bipartidas com cores deepskyblue e limegreen no grafo
        draw_bipart(groupA, 'deepskyblue', G_pgv, arvore)
        draw_bipart(groupB, 'limegreen', G_pgv, arvore)
        print("Grupo A: ",groupA," Grupo B: ",groupB)


# Função para desenhar componentes do grafo
def draw_components(G_pgv, componentes):
    colors = ['green', 'blue', 'pink', 'orange', 'violet']

    # Função interna para desenhar os nós de um componente com uma cor específica
    def draw_nodes(nodes, color, G=G_pgv):
        for node in nodes:
            pgv_node = G.get_node(node)
            pgv_node.attr['color'] = color

    for componente in componentes:
        # Desenha cada componente com uma cor diferente no grafo
        draw_nodes(componente, colors.pop(), G_pgv)

    G_pgv.draw('grafo/grafo.png')

# Função para colocar uma aresta na árvore de busca em largura
def colocar_arv(arvore, pai, filho, cor="black"):
    if arvore is not None:
        if pai is None:
            arvore.add_node(filho)

        elif str(pai) in arvore.nodes() and str(filho) in arvore.nodes():
            #Se o pai e o filho estiver na árvore cria uma aresta especial a qual não influência no layout
            arvore.add_edge(pai, filho, color=cor, constraint=False)
        else:
            arvore.add_node(pai)
            arvore.add_node(filho)
            arvore.add_edge(pai, filho, color=cor)

        arvore.graph_attr.update(rankdir='TB')
        arvore.node_attr.update(style='filled', shape='circle', width='0.3', height='0.3', fixedsize='True',
                                color='lightblue')
        arvore.edge_attr.update(penwidth='3.0')
        arvore.layout(prog='dot')

        arvore.draw('grafo/arvore.png')

        return arvore
    else:
        return None

# Função para atualizar a visualização do grafo, marcando vértices e arestas com cores específicas
def atualizar_grafo(G_pgv=None, no_atual=None, no_visitados=None, arestas_visitadas=None,
                    aresta_pintada=None,vertices_enfileirados = None):
    def draw_edges(edges, color, width, G=G_pgv):
        for edge in edges:
            pgv_edge = G.get_edge(*edge)
            pgv_edge.attr['color'] = color
            pgv_edge.attr['penwidth'] = width

    if arestas_visitadas:
        draw_edges(arestas_visitadas, 'red', 3.0)

    if aresta_pintada:
        draw_edges([aresta_pintada], 'green', 3.0)

    def draw_nodes(nodes, color, G = G_pgv):
        for node in nodes:
            pgv_node = G.get_node(node)
            pgv_node.attr['color'] = color

    try:
        if no_visitados is not None and vertices_enfileirados is not None:
            #tira os nós visitados dos nós enfirelados para que sejam coloridos de forma diferente
            resultado = list(set(no_visitados) - set(vertices_enfileirados))
        else:
            resultado = None

        if resultado:
            draw_nodes(resultado, '#FF2E2E')

        if vertices_enfileirados is not None:
            draw_nodes(vertices_enfileirados, 'skyblue')

        if no_atual is not None:
            draw_nodes([no_atual], '#63FF5C')
    except:
        pass

    G_pgv.draw('grafo/grafo.png')

    #return G_pgv

# Função para zerar as cores do grafo, deixando todos os vértices e arestas cinza e pretas, respectivamente
def zerar_cor_grafo(G_pgv):
    for node in G_pgv.nodes():
        node.attr['color'] = 'gray'

    for edge in G_pgv.edges():
        edge.attr['color'] = 'black'

    G_pgv.draw('grafo/grafo.png')
