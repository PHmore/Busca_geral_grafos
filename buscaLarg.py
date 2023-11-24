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

import networkx as nx
import matplotlib.pyplot as plt

def gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem, arestas_visitadas=None, aresta_pintada=None):
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

    # Desenha todas as arestas do grafo
    nx.draw_networkx_edges(G, pos, ax=ax, width=1.0, alpha=0.5, edge_color='k')

    # Se houverem arestas visitadas, desenha-as em vermelho
    if arestas_visitadas:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=arestas_visitadas,
                               width=2.0, edge_color='red')

    # Se houver uma aresta pintada, desenha-a em verde
    if aresta_pintada:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[aresta_pintada],
                               width=2.0, edge_color='green')

    # Desenha os nós, rótulos e salva a imagem
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=700, node_color="skyblue")
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color="black", font_weight="bold")

    plt.savefig(caminho_imagem, format="png", bbox_inches="tight")
    plt.close()
    return arestas



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

lista = matriz_adjacencia_para_lista(matriz_adjacencia_exemplo)
calcular_grau(lista)

for vertice, grau in lista.items():
    print(f'O vértice {vertice} possui grau {grau}')

caminho_imagem_saida = "grafo/grafo.png"
caminho_imagem = "grafo/grafo.png"
sg.theme('Reddit')

arestas_visitada = [(1,4),(1,8),(1,6)]

gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem,arestas_visitada,(1,3))


# Exemplo: criar uma fila com tamanho variável de 8
tamanho = 8

layout = [[sg.Image(key="-IMAGE-")],
          [sg.Button('Busca')],
          [sg.Graph(canvas_size=(400, 50), graph_bottom_left=(0, 0), graph_top_right=(400, 50), key='graph')]]

window = sg.Window('Busca em Largura', layout, resizable=True, finalize=True)

graph = window['graph']
largura_celula = 400 // tamanho  # Divide a largura pelo número de elementos na fila
altura_celula = 50

for i in range(tamanho):
    graph.draw_rectangle((i * largura_celula, 0), (i * largura_celula + largura_celula, altura_celula),
                         line_color='black')

while True:
    window["-IMAGE-"].update(filename=caminho_imagem)
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Read':
        window['-IN-'].update('')

    if event == 'Busca':
        # Minha versão da busca em largura
        fila = list()
        vertices = list()

        # Cria um nó para todos os vértices e aloca todos em uma lista
        arestas = gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem_saida)
        num_vertices = 1
        for v in arestas:
            novo_no = Vertice(num_vertices)
            num_vertices = num_vertices + 1
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
        primeiro_vertice = 1
        fila.append(vertices[primeiro_vertice - 1])
        vertices[primeiro_vertice - 1].marcado = True

        while fila:
            for vizinho in vertices[primeiro_vertice - 1].adjacencia:  # Para a vizinhança de v
                if not vertices[vizinho - 1].marcado:  # Se w não estiver marcado
                    aresta_escolhida = (vertices[primeiro_vertice - 1].numero, vizinho)  # Visitar (v, w)
                    vertices[vizinho - 1].marcado = True  # Marcar w
                    fila.append(vertices[vizinho - 1])  # Inserir w em Q

                    print(vertices[vizinho - 1].numero, vertices[vizinho - 1].marcado, vertices[vizinho - 1].adjacencia)
                else:
                    if vertices[vizinho - 1] in fila:  # Se w em Q
                        aresta_escolhida = (vertices[primeiro_vertice - 1].numero, vizinho)  # Visitar (v, w)

            gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem_saida, aresta_escolhida)  # Gera imagem
            del fila[0]  # retirar v de Q

            print('------Fila:')
            for ver in range(0, len(fila)):
                print(fila[ver].numero, fila[ver].marcado, fila[ver].adjacencia)
            print('-----------')

            arestas_visitada.append((1,3))
            gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem,arestas_visitada,(3,4))


"""
Algoritmo de busca em largura na implementação

Data: Grafo G(V,E), conexo
v = vértice, w = vizinho de v, A(v) = vizinhança de v, Q = fila

#lembrando que a fila começara com o nó raiz antes de entrar no algoritmo

while Fila != NULL faça:
     for w pertecente a A(v) faça:
        if w não marcado então:
            visitar(v,w);
            marcar(w);
            inserir(w) em Q;
            
            criar nó(w) na árvore e definir v como seu pai e atribuir nível = variável
        else 
            if w pertence a fila então:
                visitar (v,w) #! aresta de cruzamento

                verificar nível dos nós verificar se v e w possuem o mesmo pai, pois cada situação gerará um tipo de aresta
            end
        end
    end
    retirar v de Q
end



Algoritmo de busca em largura

Data: Grafo G(V,E), conexo
v = vértice, w = vizinho de v, A(v) = vizinhança de v, Q = fila

while Fila != NULL faça:
     for w pertecente a A(v) faça:
        if w não marcado então:
            visitar(v,w);
            marcar(w);
            inserir(w) em Q;
        else 
            if w pertence a fila então:
                visitar (v,w) #! aresta de cruzamento
            end
        end
    end
    retirar v de Q
end

OBSERVAÇÕES: se quando w for encontrado v não estiver na fila não será feito nada pois provavelmente
já existe uma aresta ligando w e v, caso v esteja na lista será feito uma aresta, se ambos estiver no mesmo nível e ter o mesmo pai
será uma aresta irmão se não tiver o mesmo pai será uma aresta primo e se não tiver no mesmo nível será uma aresta tio
"""
