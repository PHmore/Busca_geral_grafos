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

def gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem, no_atual = None,no_visitados = None,arestas_visitadas=None, aresta_pintada=None):
    G = nx.Graph()

    # Converta a matriz de adjacência em uma lista de arestas
    arestas = []
    for i in range(len(matriz_adjacencia)):
        for j in range(len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] == 1:
                # Ajuste para iniciar a contagem dos vértices do 1
                arestas.append((i + 1, j + 1))

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
        print(resultado)
    else: 
        resultado = None 

    if resultado:
        draw_nodes(resultado, '#FF2E2E')
    
    if vertices_enfileirados:
        draw_nodes(vertices_enfileirados, 'skyblue')

    if no_atual:
        draw_nodes([no_atual], '#63FF5C')

    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color="black", font_weight="bold")

    plt.savefig(caminho_imagem, format="png", bbox_inches="tight")
    plt.close()
    return arestas

def colocar_arv (arvore, pai, filho, cor = "k"):
    if not arvore.has_node(filho):
        arvore.add_node(filho)
    if arvore.has_node(pai):
        arvore.add_edge(pai, filho, color=cor)
    else:
        print("Erro: O nó pai não existe na árvore.")
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

def buscar_em_largura(vertice_inicial=None,arvore = None):
    global vertices_enfileirados
    
    vertices_visitados = list ()
    vertices = list()
    arestas_visitadas = list()

    # Cria um nó para todos os vértices e aloca todos em uma lista
    arestas = gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem_saida)
    num_vertices = 1
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
    primeiro_vertice = 2
    fila = deque([vertices[primeiro_vertice - 1]])
    vertices[primeiro_vertice - 1].marcado = True
    vertices_enfileirados.append(vertices[primeiro_vertice - 1].numero)
    vertices_visitados.append(vertices[primeiro_vertice - 1].numero)
    colocar_arv(arvore,None,primeiro_vertice)

    while fila:
        vertice_atual = fila.popleft()
        
        #Para cada vizinho
        for vizinho in vertice_atual.adjacencia:

            #Se não tiver marcado
            if not vertices[vizinho - 1].marcado:
                aresta_escolhida = (vertice_atual.numero, vizinho)
                arestas_visitadas.append(aresta_escolhida)
                vertices[vizinho - 1].marcado = True
                fila.append(vertices[vizinho - 1])
                vertices_enfileirados.append(vertices[vizinho - 1].numero)
                vertices_visitados.append(vertices[vizinho - 1].numero)
                gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem_saida, vertice_atual.numero, vertices_visitados,
                                      arestas_visitadas, aresta_escolhida)  # Gera imagem
                window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
                window['-IMAGE-'].update(f'{caminho_imagem}')
                window.refresh()
            else:
                if vertices[vizinho - 1] in fila:
                    aresta_escolhida = (vertice_atual.numero, vizinho)
                    arestas_visitadas.append(aresta_escolhida)
                    gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem_saida, vertice_atual.numero, vertices_visitados,
                                      arestas_visitadas, aresta_escolhida)  # Gera imagem
                    window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window.refresh()

                window["-IMAGE2-"].update(filename="grafo/arvore.png")
                window.refresh()

        vertices_enfileirados.pop(0)


        

    gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem_saida, vertice_atual.numero, vertices_visitados,
                                      arestas_visitadas, aresta_escolhida)  # Gera imagem
    window["-TEXT-"].update(f'Vertices: {vertices_enfileirados}')
    window['-IMAGE-'].update(f'{caminho_imagem}')
    window["-IMAGE2-"].update(filename="grafo/arvore.png")
    window.refresh()
    #time.sleep(1)


# Exemplo: gerar uma imagem do grafo
matriz_adjacencia_exemplo = [
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

caminho_imagem_saida = caminho_imagem = "grafo/grafo.png"
sg.theme('Reddit')

"""
lista = matriz_adjacencia_para_lista(matriz_adjacencia_exemplo)
calcular_grau(lista)

for vertice, grau in lista.items():
    print(f'O vértice {vertice} possui grau {grau}')
"""

arvore = nx.Graph()

vertices_enfileirados = list()
layout = [[sg.Column([[sg.Image(key="-IMAGE-")]]),
          sg.Column([[sg.Image(key="-IMAGE2-")]])],
          [sg.Push(), sg.Button('Busca'), sg.Push()],
          [sg.Text(f'Fila: {vertices_enfileirados}', key="-TEXT-")]
          ]

window = sg.Window('Busca em Largura', layout, resizable=True, finalize=True)

while True:
    window["-IMAGE-"].update(filename=caminho_imagem)
    window["-IMAGE2-"].update(filename="grafo/arvore.png")
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Read':
        window['-IN-'].update('')
        window.Refresh()

    if event == 'Busca':
        buscar_em_largura(None,arvore)
        window.Refresh()