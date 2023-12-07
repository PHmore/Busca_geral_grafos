# Importa as bibliotecas necessárias
import time
from collections import deque
import pygraphviz as pgv
from funGrafo import *


# Função para zerar as cores do grafo, deixando todos os vértices e arestas cinza e pretas, respectivamente
def zerar_cor_grafo(G_pgv):
    for node in G_pgv.nodes():
        node.attr['color'] = 'gray'

    for edge in G_pgv.edges():
        edge.attr['color'] = 'black'

    G_pgv.draw('grafo/grafo.png')


# Função para atualizar a visualização do grafo, marcando vértices e arestas com cores específicas
def atualizar_grafo(G_pgv=None, no_atual=None, no_visitados=None, arestas_visitadas=None,
                    aresta_pintada=None):
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


# Função para realizar a busca em largura em um grafo e visualizar a árvore resultante
def buscar_em_largura(G_pgv, caminho_imagem, vertices, vertices_visitados, arestas_irmao, arestas_primo,
                      arestas_pai, arestas_tio, window=None, vertice_inicial=0, arvore=None, componentes=[],
                      sleep_t=0.5):
    arestas = []
    arestas_visitadas = list()

    arestas = list(G_pgv.edges())
    arestas = [(int(aresta[0]), int(aresta[1])) for aresta in arestas]

    #função para ver a quantidade de vértices e inicializa-los
    num_vertices = list()
    for v in range(len(G_pgv.nodes())):
        num_vertices.append(v)
        if len(vertices) <= v:
            novo_no = Vertice(v, -1)
            vertices.append(novo_no)

    #função para inicializar a vizinhança de cada vértice
    for v in vertices:
        for n in arestas:
            if v.numero in n:
                if n[0] == v.numero and n[1] not in v.adjacencia:
                    v.adjacencia.append(n[1])
                elif n[1] == v.numero and n[0] not in v.adjacencia:
                    v.adjacencia.append(n[0])
        v.adjacencia.sort()

    #adiciona e marca o vértice inicial
    fila = deque([vertices[vertice_inicial]])
    vertices[vertice_inicial].marcado = True
    vertices[vertice_inicial].nivel_na_arvore = 1

    if window:
        vertices_enfileirados.append(vertices[vertice_inicial].numero)
    vertices_visitados.append(vertices[vertice_inicial].numero)

    colocar_arv(arvore, None, vertice_inicial)
    vertices[vertice_inicial].numero_pai = None

    #Enquanto houver uma fila
    while fila:
        vertice_atual = fila.popleft()

        #Para cada vizinho do vertice da fila
        for vizinho in vertice_atual.adjacencia:

            #Se não tiver marcado será feito uma aresta pai
            if not vertices[vizinho].marcado:
                aresta_escolhida = (vertice_atual.numero, vizinho)
                arestas_visitadas.append(aresta_escolhida)
                vertices[vizinho].marcado = True
                fila.append(vertices[vizinho])

                if window:
                    vertices_enfileirados.append(vertices[vizinho].numero)

                vertices_visitados.append(vertices[vizinho].numero)
                arestas_pai.append(aresta_escolhida)
                colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero)
                vertices[vizinho].numero_pai = vertice_atual.numero
                vertices[vizinho].nivel_na_arvore = vertice_atual.nivel_na_arvore + 1

                if window:
                    atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                                    arestas_visitadas, aresta_escolhida)
                    window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window['-IMAGE2-'].update(f'{"grafo/arvore.png"}')
                    window.refresh()
                    time.sleep(sleep_t)

            #Se estiver marcado
            else:

                #Se estiver na fila
                if vertices[vizinho] in fila:
                    aresta_escolhida = (vertice_atual.numero, vizinho)
                    arestas_visitadas.append(aresta_escolhida)

                    #Se tiver o mesmo pai será feito uma aresta irmão
                    if (vertice_atual.numero_pai == vertices[vizinho].numero_pai):
                        arestas_irmao.append(aresta_escolhida)
                        colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero, "DarkBlue")

                    #Se tiver o mesmo nível será feito uma aresta primos
                    elif (vertice_atual.nivel_na_arvore == vertices[vizinho].nivel_na_arvore):
                        arestas_primo.append(aresta_escolhida)
                        colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero, "orange")

                    #Em último caso será feito uma aresta tio
                    else:
                        arestas_tio.append(aresta_escolhida)
                        colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero, "DarkMagenta")

                    if window:
                        atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                                        arestas_visitadas, aresta_escolhida)
                        window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
                        window['-IMAGE-'].update(f'{caminho_imagem}')
                        window['-IMAGE2-'].update(f'{"grafo/arvore.png"}')
                        window.refresh()
                        time.sleep(sleep_t)
                elif window:
                    atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                                    arestas_visitadas)
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window["-IMAGE2-"].update(filename="grafo/arvore.png")
                    window.refresh()
                    time.sleep(sleep_t)

        if window:
            vertices_enfileirados.pop(0)
            window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')

    if window:
        atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                        arestas_visitadas)
        window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
        window['-IMAGE-'].update(f'{caminho_imagem}')
        window["-IMAGE2-"].update(filename="grafo/arvore.png")
        window.refresh()

    #Verifica se é conexo retornando os vértices não encontrados ainda
    G_conn = isConnect(vertices_visitados, num_vertices, componentes)

    if not G_conn:
        return False
    else:
        #Realiza a busca novamente começando agora pelo vértice da componente desconexa
        buscar_em_largura(G_pgv, caminho_imagem, vertices, vertices_visitados, arestas_irmao, arestas_primo,
                          arestas_pai, arestas_tio, window, G_conn[0], arvore, componentes, sleep_t)
        return True


# Função para criar a interface gráfica da busca em largura
def interface_buscaLarg(G_pgv, matriz_adjacencia):
    global vertices_enfileirados

    # Caminho para a imagem do grafo
    caminho_imagem = "grafo/grafo.png"
    sg.theme('Reddit')

    # Zera as cores do grafo e cria uma árvore vazia
    zerar_cor_grafo(G_pgv)
    arvore = pgv.AGraph(strict=True)
    arvore.layout(prog='dot')
    arvore.draw('grafo/arvore.png')

    # Listas para armazenar informações sobre as arestas
    arestas_primo = list()
    arestas_tio = list()
    arestas_pai = list()
    arestas_irmao = list()

    # Listas para armazenar informações sobre os vértices
    vertices = list()
    vertices_enfileirados = list()
    vertices_visitados = list()

    # Layout da interface gráfica
    layout = [
        [
            sg.Column([
                        [sg.Text('Legenda de vértices:')],
                        [sg.Text('', background_color='green'), sg.Text('Em processo de visita ', pad=(0, 0))],
                        [sg.Text('', background_color='skyblue'), sg.Text('Marcado ', pad=(0, 0))],
                        [sg.Text('', background_color='red'), sg.Text('Totalmente explorados ', pad=(0, 0))],
                        [sg.Text(''), sg.Text(''), sg.Text(''), sg.Text('')],
                        [sg.Text('Legenda de arestas:')],
                        [sg.Text('', background_color='green'), sg.Text('Em processo de visita ', pad=(0, 0))],
                        [sg.Text('', background_color='red'), sg.Text('Visitadas ', pad=(0, 0))]
                    ],vertical_alignment='center'),

            sg.Column([
                [sg.Image(filename=caminho_imagem, key="-IMAGE-")],
                [sg.Text(f'Fila: {vertices_enfileirados}', key="-TEXT-", font=("Ubuntu", 20))]
                
            ]),

            sg.VSeparator(),
            sg.Column([
                [sg.Text(f'Arvore', font=("Ubuntu", 20))],
                [sg.Text(''), sg.Text(''), sg.Text(''), sg.Text('')],
                [sg.Text('Legenda de arestas:')],
                [sg.Text('', background_color='black'), sg.Text('Pai ', pad=(0, 0))],
                [sg.Text('', background_color='DarkBlue'), sg.Text('Irmão ', pad=(0, 0))],
                [sg.Text('', background_color='DarkMagenta'), sg.Text('Tio ', pad=(0, 0))],
                [sg.Text('', background_color='orange'), sg.Text('Primo ', pad=(0, 0))],
                [sg.Text(''), sg.Text('')]

            ], vertical_alignment='center'),
            sg.Column([
                [sg.Image(filename="grafo/arvore.png", key="-IMAGE2-")]
            ])
        ],
        [sg.HSeparator()],
        [
            sg.Push(),
            sg.Column([[sg.Button('Mostrar bipartição', visible=False)]], key='-COL-BPART-'),
            sg.Button('Busca'),
            sg.Button('Sair'),
            sg.Push()
        ]
    ]

    # Criação da janela
    window = sg.Window('Busca em Largura', layout, resizable=True, finalize=True, auto_size_buttons=True,
                       auto_size_text=True)

    while True:
        event,values = window.read()

        # Verifica se a janela foi fechada ou o botão 'Sair' foi pressionado
        if event == sg.WIN_CLOSED or event == 'Sair':
            zerar_cor_grafo(G_pgv)
            break
            

        # Verifica se o botão 'Busca' foi pressionado
        if event == 'Busca':

            # Limpa as listas e obtém o vértice inicial
            arestas_primo.clear()
            arestas_tio.clear()
            arestas_pai.clear()
            arestas_irmao.clear()
            vertices.clear()
            vertices_enfileirados.clear()
            vertices_visitados.clear()
            vertice_inicial = vert_inicial(matriz_adjacencia)

            # Verifica se um vértice inicial foi selecionado
            if vertice_inicial != -1:
                arvore.clear()
                zerar_cor_grafo(G_pgv)
                # Realiza a busca em largura
                buscar_em_largura(G_pgv, caminho_imagem, vertices, vertices_visitados,
                                  arestas_irmao, arestas_primo, arestas_pai, arestas_tio, window, vertice_inicial, arvore, [], 1.0)
                # Torna visível o botão 'Mostrar bipartição'
                window['-COL-BPART-'].update(visible=True)
                window['Mostrar bipartição'].update(visible=True)

                print("\nArestas pai: ",arestas_pai,"\nArestas irmão: ",arestas_irmao,
                  "\nArestas primo: ",arestas_primo,"\nArestas tio: ",arestas_tio,"\n")


        # Exibe informações sobre as arestas
        if event == 'Mostrar bipartição':
            isBipart(vertices, arestas_irmao, arestas_primo, arvore, G_pgv)
            arvore.clear()
            window["-IMAGE2-"].update(filename="grafo/arvore.png")
            window["-IMAGE-"].update(filename="grafo/grafo.png")

    window.close()
    return

