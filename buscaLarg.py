# Aqui será feita a busca em largura OBS: A busca deve ser realizada mesmo que o usuário selecione a opção 3

"""
6 – Caso o usuário selecione a opção “2” o programa deve perguntar: “Qual será o vértice raiz da
busca?” e apresentar a listagem dos vértices candidatos; Na sequência deve-se ser apresentada a
árvore de busca em largura e apresentar pelo menos o ponto em que foi identificado que o grafo não
seria Bipartido, no caso de o grafo não ser;

** O algoritmo de reconhecimento deve utilizar a Busca em Largura tal como foi estudada em sala
de aula;
*** Os conjuntos de arestas geradas pela busca em largura devem ser apresentados.
"""
import time

# ! Gera o grafo e o salva como imagem
import networkx as nx
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from Vertice import Vertice
from funGrafo import *
from lerGrafo import *
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

#! Talvez seja interessante deixa escolher qualquer vértice pois se o grafo for desconexo ele gera duas arvores
#! Esse mesmo fator pode ser usado para mostrar as componentes desconexas por meio de arvores e 
#!usando set para cada componente e comporando a quantidade de vértices encontrados com a quantidade de nós totais

#! Verificar porque uma aresta verde permanece, e resolver para não gerar confusão na visualização

#! Tentar fazer com que sair no meio do programa não mostre a tela de morte

#! É totalmente viável usar apenas o gerar imagem que está sendo usado nessa função, pois a imagem é mais bonita
#!,porém ser o grafo for desconexo com uma componente sendo um K1 a imagem do gerar dessa função não o mostra (Resolver)

#! Estudar o uso da biblioteca que gera a imagem da árvore para gerar a imagem do grafo

def calcular_grau_vertice(matriz_adjacencia):
    graus = []
    num_vertices = len(matriz_adjacencia)

    for i in range(num_vertices):
        grau = 0
        for j in range(num_vertices):
            if matriz_adjacencia[i][j] == 1:
                grau += 1
        graus.append(grau)

    dados_tabela = []
    for idx, grau in enumerate(graus):
        dados_tabela.append([f'{idx}', grau])

    dados_tabela.sort(key=lambda x: x[1], reverse=True)
    dados_tabela = dados_tabela[:3]
    return dados_tabela

def vert_inicial(grafo):
    # Dados da tabela (vértices e graus)
    dados_tabela = calcular_grau_vertice (grafo)

    # Layout da janela
    layout = [
        [sg.Table(values=dados_tabela, headings=['Vértice', 'Grau'], auto_size_columns=True, key='-TABLE-')],
        [sg.Text("Quanto maior o grau mais eficiente a busca", key='-MESSAGE-')],
        [sg.Text('Selecione um item:'), sg.Combo(values=[row[0] for row in dados_tabela], key='-COMBO-')],
        [sg.Button('OK'), sg.Button('Cancelar')]
    ]

    window = sg.Window('Interface', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break

        if event == 'OK':
            selected_vertex = values['-COMBO-']
            break
            

    window.close()
    return int(selected_vertex)

def gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem, no_atual = None,no_visitados = None,arestas_visitadas=None, aresta_pintada=None):
    G = nx.Graph()

    # Converta a matriz de adjacência em uma lista de arestas
    arestas = []
    for i in range(len(matriz_adjacencia)):
        for j in range(len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] == 1:
                # Ajuste para iniciar a contagem dos vértices do 1
                arestas.append((i, j))

    G.add_edges_from(arestas)
    fig, ax = plt.subplots()

    pos = nx.spring_layout(G, seed=42)  # Posicionamento dos nós

    # Função para desenhar arestas com base na cor e na lista de arestas
    def draw_edges(edges, color, width):
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges, width=width, edge_color=color)

    # Desenha todas as arestas do grafo em preto
    draw_edges(G.edges(), 'k', 1.0)

    # Se houverem arestas visitadas, desenha-as em vermelho
    if arestas_visitadas:
        draw_edges(arestas_visitadas, 'red', 2.0)

    # Se houver uma aresta pintada, desenha-a em verde
    if aresta_pintada:
        draw_edges([aresta_pintada], 'green', 2.0)

    def draw_nodes(nodes, color):
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=nodes, node_size=700, node_color=color)

    # Desenha os nós, rótulos e salva a imagem
    draw_nodes(G.nodes(), 'gray')

    if no_visitados and vertices_enfileirados:
        resultado = list(set(no_visitados)-set(vertices_enfileirados))
    else: 
        resultado = None 

    if resultado:
        draw_nodes(resultado, '#FF2E2E')
    
    if vertices_enfileirados:
        draw_nodes(vertices_enfileirados, 'skyblue')
    if no_atual is not None:
        draw_nodes([no_atual], '#63FF5C')

    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color="black", font_weight="bold")

    plt.savefig(caminho_imagem, format="png", bbox_inches="tight")
    plt.close()
    return arestas

def colocar_arv (arvore, pai, filho, cor = "black"):
    #! Depois tratar corretamente pois nem todo vértice é pai seria interessante nomear de no1 e no2 as entradas
    if not arvore.has_node(filho):
        arvore.add_node(filho)
    if arvore.has_node(pai):
        arvore.add_edge(pai, filho, color=cor)
    else:
        print("Erro: nó pai não existe na árvore.")
        arvore.add_node(filho)
        print("Portanto o nó foi adicionado como filho")


    # Converter para um grafo PyGraphviz
    G = nx.nx_agraph.to_agraph(arvore)

    # Configuração de tamanho para nós e arestas
    G.graph_attr.update(rankdir='TB')
    G.node_attr.update({'style': 'filled', 'shape': 'circle', 'width': '0.1', 'height': '0.1','color':'skyblue'})  # Ajuste de tamanho dos nós
    G.edge_attr.update({'penwidth': '3.0'})  # Ajuste de largura das arestas

    # Layout e geração da imagem com Graphviz
    G.layout(prog='dot')
        
    G.draw('grafo/arvore.png')
    return arvore

def buscar_em_largura(window,caminho_imagem,matriz_adjacencia, vertice_inicial=None,arvore = None, ):
    #Declarando variáveis
    
    vertices_visitados = list ()
    vertices = list()
    arestas_visitadas = list()

    #Obtem por meio da leitura do grafo as arestas
    arestas = gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem)

    # Cria um nó para todos os vértices e aloca todos em uma lista
    num_vertices = 0
    for v in arestas:
        novo_no = Vertice(num_vertices)
        num_vertices += 1
        vertices.append(novo_no)

    # Determina toda a vizinhança dos vértices
    for v in vertices:
        for n in arestas:
            if v.numero in n:
                if n[0] == v.numero and n[1] not in v.adjacencia:
                    v.adjacencia.append(n[1])
                elif n[1] == v.numero and n[0] not in v.adjacencia:
                    v.adjacencia.append(n[0])

    # Seja v o primeiro elemento
    #! Talvez modificar pois está contando que os vértices serão enumerados e não nomeado
    primeiro_vertice = vertice_inicial

    #Cria e insere o vértice inicial na fila duplamente encadeada e na arvóre
    fila = deque([vertices[primeiro_vertice ]])
    vertices[primeiro_vertice ].marcado = True
    vertices_enfileirados.append(vertices[primeiro_vertice ].numero)
    vertices_visitados.append(vertices[primeiro_vertice ].numero)

    #Enquanto existir a fila
    while fila:
        #Toma-se o primeiro vértice da fila
        vertice_atual = fila.popleft()
        
        #Para cada vizinho
        for vizinho in vertice_atual.adjacencia:
            
            #Se não tiver marcado
            if not vertices[vizinho ].marcado:
                #Visita a aresta
                aresta_escolhida = (vertice_atual.numero, vizinho)
                arestas_visitadas.append(aresta_escolhida)
                #Marca o vertice
                vertices[vizinho ].marcado = True
                #Adiciona na fila
                fila.append(vertices[vizinho ])
                vertices_enfileirados.append(vertices[vizinho ].numero)
                vertices_visitados.append(vertices[vizinho ].numero)
                #Adiciona na árvore com aresta pai
                colocar_arv(arvore,vertice_atual.numero,vertices[vizinho].numero)

                # criar nó(w) na árvore e definir v como seu pai e atribuir nível = variável
                gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem, vertice_atual.numero, vertices_visitados,
                                      arestas_visitadas, aresta_escolhida)  # Gera imagem
                window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
                window['-IMAGE-'].update(f'{caminho_imagem}')
                window['-IMAGE2-'].update(f'{"grafo/arvore.png"}')
                window.refresh()
                time.sleep(1)
            else:
                #Se estiver marcado e estiver na fila
                if vertices[vizinho] in fila:
                    #Visita a aresta
                    aresta_escolhida = (vertice_atual.numero, vizinho)
                    arestas_visitadas.append(aresta_escolhida)

                    #! Aresta Especial
                    # verificar nível dos nós e verificar se v e w possuem o mesmo pai, pois cada situação gerará um tipo de aresta
                    """
                    Talvez seja bom para o nível fazer vértice.nivel = vertice.pai.vivel + 1, pois assim se manterá nivelado

                    if(vertice.pai == vertice.vizinho.pai)
                    {
                    aresta irmão
                    }
                    else if (vertice.nivel == vertice.vizinho.nivel)
                    {
                    aresta de primo
                    } else 
                    {
                    aresta de tio
                    }
                    """

                    gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem, vertice_atual.numero, vertices_visitados,
                                      arestas_visitadas, aresta_escolhida)  # Gera imagem
                    window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window['-IMAGE2-'].update(f'{"grafo/arvore.png"}')
                    window.refresh()
                    time.sleep(1)
                #Caso já esteja marcado e fora da fila não fará nada
                #Tanto que tlvz possa até tirar o else e todo bloco de código dele
                else:
                    gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem, vertice_atual.numero, vertices_visitados,
                                        arestas_visitadas, aresta_escolhida)  # Gera imagem
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window["-IMAGE2-"].update(filename="grafo/arvore.png")
                    window.refresh()
                    time.sleep(1)
        #Remove da fila
        vertices_enfileirados.pop(0)

#Como se repete enquanto houver uma fila irá visitar todos os vértices sequencialmente


        

    gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem, vertice_atual.numero, vertices_visitados,
                                      arestas_visitadas, aresta_escolhida)  # Gera imagem
    window["-TEXT-"].update(f'Vertices: {vertices_enfileirados}')
    window['-IMAGE-'].update(f'{caminho_imagem}')
    window["-IMAGE2-"].update(filename="grafo/arvore.png")
    window.refresh()
    #time.sleep(1)

def interface_buscaLarg(grafo):
    global vertices_enfileirados
# Exemplo: gerar uma imagem do grafo
    matriz_adjacencia = grafo
    """
    matriz_adjacencia = [
        [0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 1, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
    ]
"""

    caminho_imagem = caminho_imagem = "grafo/grafo.png"
    sg.theme('Reddit')

    """
    lista = matriz_adjacencia_para_lista(matriz_adjacencia)
    calcular_grau(lista)

    for vertice, grau in lista.items():
        print(f'O vértice {vertice} possui grau {grau}')
    """
    vertice_inicial = vert_inicial(matriz_adjacencia)
    arvore = nx.Graph()
    print(arvore)
    colocar_arv(arvore,None,vertice_inicial)

    vertices_enfileirados = list()
    layout = [[sg.Column([[sg.Image(filename=caminho_imagem,key="-IMAGE-")]]),
            sg.Column([[sg.Image(filename="grafo/arvore.png",key="-IMAGE2-")]])],
            [sg.Push(), sg.Button('Busca'), sg.Push(),sg.Button('Sair')],
            [sg.Button('Mudar vertice inicial')],
            [sg.Text(f'Fila: {vertices_enfileirados}', key="-TEXT-")]
            ]

    window = sg.Window('Busca em Largura', layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Sair':
            break

        if event == 'Read':
            window['-IN-'].update('')
            window.Refresh()

        if event == 'Busca':
            
            buscar_em_largura(window,caminho_imagem,matriz_adjacencia,vertice_inicial,arvore)
            #talvez retorna o vértice o qual a bipartição é nula
            window.Refresh()

        if event == 'Mudar vertice inicial':
            __import__('os').remove('grafo/arvore.png')
            #! Falta fazer com que o vértice inicial entre
            #! Talvez remover tudo e deixar como antes
            #! Focar em realizar a busca a grafos desconexos automaticamente
            vertice_inicial = vert_inicial(matriz_adjacencia)
            arvore.clear()
            window.Refresh()


    return

#interface_buscaLarg(None)