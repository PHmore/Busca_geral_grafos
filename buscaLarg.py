import time
from collections import deque
import pygraphviz as pgv
from funGrafo import *
import os

# ! Tentar fazer com que sair no meio do programa não mostre a tela de morte

# Tlvz seja possível retirar a repetição de definição de listas
# Visto que no python as alterações em listas dentro de funções são globais

def zerar_cor_grafo(G_pgv):

    for node in G_pgv.nodes():
        node.attr['color'] = 'gray'

    for edge in G_pgv.edges():
        edge.attr['color'] = 'black'
    
    G_pgv.draw('grafo/grafo.png')

def atualizar_grafo(G_pgv = None, no_atual=None, no_visitados=None, arestas_visitadas=None,
                          aresta_pintada=None):
    
    def draw_edges(edges, color, width, G = G_pgv):
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

def colocar_arv(arvore, pai, filho, cor="black"):
    if arvore is not None:
        if pai == None:
            arvore.add_node(filho)
        
        elif str(pai) in arvore.nodes() and str(filho) in arvore.nodes():
            arvore.add_edge(pai, filho, color=cor, constraint = False)
        else:
            arvore.add_node(pai)
            arvore.add_node(filho)
            arvore.add_edge(pai, filho, color=cor)
    
        arvore.graph_attr.update(rankdir='TB')
        arvore.node_attr.update(style='filled', shape='circle', width='0.3', height='0.3', fixedsize='True', color='lightblue')
        arvore.edge_attr.update(penwidth='3.0')
        arvore.layout(prog='dot')
        
        arvore.draw('grafo/arvore.png')

        return arvore
    else:
        return None


def buscar_em_largura(G_pgv,caminho_imagem,vertices, vertices_visitados, arestas_irmao,arestas_primo,arestas_pai,arestas_tio,window = None, vertice_inicial=0,arvore = None,componentes = [] ):
    arestas = []
    arestas_visitadas = list()

    arestas = list(G_pgv.edges())
    arestas = [(int(aresta[0]), int(aresta[1])) for aresta in arestas ]

    num_vertices = list()
    for v in range(len(G_pgv.nodes())):
        num_vertices.append(v)
        if len(vertices) <= v:
            novo_no = Vertice(v,-1)
            vertices.append(novo_no)
            
    for v in vertices:
        for n in arestas:
            if v.numero in n:
                if n[0] == v.numero and n[1] not in v.adjacencia:
                    v.adjacencia.append(n[1])
                elif n[1] == v.numero and n[0] not in v.adjacencia:
                    v.adjacencia.append(n[0])

    fila = deque([vertices[vertice_inicial]])
    vertices[vertice_inicial].marcado = True
    vertices[vertice_inicial].nivel_na_arvore = 1 
    if window:
        vertices_enfileirados.append(vertices[vertice_inicial].numero)
    vertices_visitados.append(vertices[vertice_inicial].numero)
    
    colocar_arv(arvore, None, vertice_inicial)
    vertices[vertice_inicial].numero_pai = None
    
    while fila:

        vertice_atual = fila.popleft()

        for vizinho in vertice_atual.adjacencia:

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
                                        arestas_visitadas, aresta_escolhida)  # Gera imagem
                    window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window['-IMAGE2-'].update(f'{"grafo/arvore.png"}')
                    window.refresh()
                    time.sleep(0.5)
            else:
                if vertices[vizinho] in fila:
                    aresta_escolhida = (vertice_atual.numero, vizinho)
                    arestas_visitadas.append(aresta_escolhida)

                    if (vertice_atual.numero_pai == vertices[vizinho].numero_pai):
                        arestas_irmao.append(aresta_escolhida)
                        colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero, "DarkBlue")

                    elif (vertice_atual.nivel_na_arvore == vertices[vizinho].nivel_na_arvore):
                        arestas_primo.append(aresta_escolhida)
                        colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero, "orange")

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
                        time.sleep(0.5)
                elif window:
                    atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                                        arestas_visitadas)
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window["-IMAGE2-"].update(filename="grafo/arvore.png")
                    window.refresh()
                    time.sleep(0.5)

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
        
    G_conn = isConnect(vertices_visitados,num_vertices,componentes)
    
    if (not G_conn):
        return False
    else:
        
        buscar_em_largura( G_pgv,caminho_imagem, vertices,vertices_visitados,arestas_irmao,arestas_primo,
                          arestas_pai,arestas_tio,window, G_conn[0], arvore,componentes)
        return True

    
        
        
        

# Mudar a direção dos dados do grafo para sua horizontal, 
# pois os grafos tendem a ser desenhados verticalmente
# Ocupando grande parte da janela
def interface_buscaLarg(G_pgv, matriz_adjacencia):
    global vertices_enfileirados

    caminho_imagem = "grafo/grafo.png"
    sg.theme('Reddit')

    arvore = pgv.AGraph(strict=True)
    arvore.layout(prog='dot')
    arvore.draw('grafo/arvore.png')

    arestas_primo = list() 
    arestas_tio = list()
    arestas_pai = list()
    arestas_irmao = list()

    vertices = list()
    vertices_enfileirados = list()
    vertices_visitados = list ()
    layout = [
        [
            sg.Column([
                [sg.Image(filename=caminho_imagem, key="-IMAGE-")],
                [sg.Text(f'Fila: {vertices_enfileirados}', key="-TEXT-", font=("Ubuntu", 20))],
                [sg.Text('Legenda de vértices:')],
                [
                    sg.Column([
                        [sg.Text('', background_color='green'), sg.Text('Em processo de visita ', pad=(0, 0))],
                        [sg.Text('', background_color='skyblue'), sg.Text('Marcado ', pad=(0, 0))],
                        [sg.Text('', background_color='red'), sg.Text('Totalmente explorados ', pad=(0, 0))]
                    ]),
                    sg.Column([
                        [sg.Text('Legenda de arestas:')],
                        [sg.Text('', background_color='green'), sg.Text('Em processo de visita ', pad=(0, 0))],
                        [sg.Text('', background_color='red'), sg.Text('Visitadas ', pad=(0, 0))]
                    ])
                ]
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
                #Colocar mensagem embaixo da arvore falando se o grafo é conexo ou não
                
            ], vertical_alignment='center'),
            sg.Column([
                [sg.Image(filename="grafo/arvore.png", key="-IMAGE2-")]
            ])
        ],
        [sg.HSeparator()],
        [
            sg.Push(), 
            sg.Column([[sg.Button('Mostrar bipartição',visible = False)]], key='-COL-BPART-'), 
            sg.Button('Busca'),
            sg.Button('Sair'), 
            sg.Push()
        ]
        ]   


    window = sg.Window('Busca em Largura', layout, resizable=True, finalize=True, auto_size_buttons=True,
                       auto_size_text=True)

    while True:
        event,values = window.read()

        if event == sg.WIN_CLOSED or event == 'Sair':
            zerar_cor_grafo(G_pgv)
            break
            

        if event == 'Read':
            window['-IN-'].update('')
            window.Refresh()

        if event == 'Busca':

            arestas_primo.clear()
            arestas_tio.clear()
            arestas_pai.clear()
            arestas_irmao.clear()
            vertices.clear()
            vertices_enfileirados.clear()
            vertices_visitados.clear()
            vertice_inicial = vert_inicial(matriz_adjacencia)

            if vertice_inicial != -1:
                arvore.clear()
                zerar_cor_grafo(G_pgv)
                buscar_em_largura( G_pgv,caminho_imagem ,vertices, vertices_visitados,
                                arestas_irmao,arestas_primo, arestas_pai,arestas_tio,window, vertice_inicial, arvore)
                window['-COL-BPART-'].update(visible=True)
                window['Mostrar bipartição'].update(visible=True)


        if event == 'Mostrar bipartição':
            isBipart(vertices, arestas_irmao, arestas_primo, arvore, G_pgv)
            arvore.clear()
            window["-IMAGE2-"].update(filename="grafo/arvore.png")
            window["-IMAGE-"].update(filename="grafo/grafo.png")
    window.close()
    return
