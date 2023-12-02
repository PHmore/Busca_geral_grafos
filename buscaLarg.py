# Aqui será feita a busca em largura OBS: A busca deve ser realizada mesmo que o usuário selecione a opção 3

#!ERROS
# Entender pq o grafo 8 não está realizando a 2 busca
import time

# ! Gera o grafo e o salva como imagem
from collections import deque
import pygraphviz as pgv
from funGrafo import *


# usando set para cada componente e comporando a quantidade de vértices encontrados com a quantidade de nós totais

# ! Tentar fazer com que sair no meio do programa não mostre a tela de morte

# ! Tlvz seja possível retirar a repetição de definição de listas
#!Visto que no python as alterações em listas dentro de funções são globais

#Consertar
def zerar_cor_grafo(G_pgv):
    print("Será feita a recoloração do grafo e arestas para gray e black")

    # Atribuir cor 'gray' para os nós
    for node in G_pgv.nodes():
        node.attr['color'] = 'gray'

    # Atribuir cor 'black' para as arestas
    for edge in G_pgv.edges():
        edge.attr['color'] = 'black'


def atualizar_grafo(G_pgv = None, no_atual=None, no_visitados=None, arestas_visitadas=None,
                          aresta_pintada=None):
    
    def draw_edges(edges, color, width, G = G_pgv):
        for edge in edges:
            pgv_edge = G.get_edge(*edge)
            pgv_edge.attr['color'] = color
            pgv_edge.attr['penwidth'] = width

    # Se houverem arestas visitadas, desenha-as em vermelho
    if arestas_visitadas:
        draw_edges(arestas_visitadas, 'red', 3.0)

    # Se houver uma aresta pintada, desenha-a em verde
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
        print("Primeira geração")
        
    G_pgv.draw('grafo/grafo.png')

    #return G_pgv


def colocar_arv(arvore, pai, filho, cor="black"):
    # Criar um novo gráfico
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
        

        # Salvar o gráfico em um arquivo de imagem
        arvore.draw('grafo/arvore.png')

        return arvore
    else:
        return None


def buscar_em_largura(G_pgv,caminho_imagem,vertices, vertices_visitados, arestas_irmao,arestas_primo,arestas_pai,arestas_tio,window = None, vertice_inicial=0,arvore = None,componentes = [] ):
    #Declarando variáveis
    arestas = []
    arestas_visitadas = list()

    #Obtem por meio da leitura do grafo as arestas
    arestas = list(G_pgv.edges())
    #Converte uma lista de strings para uma lista de inteiros
    arestas = [(int(aresta[0]), int(aresta[1])) for aresta in arestas ]
    print ("Arestas estão aqui: ",arestas)

    
        # Cria um nó para todos os vértices e aloca todos em uma lista
    num_vertices = list()
    for v in range(len(G_pgv.nodes())):
        num_vertices.append(v)
        if len(vertices) <= v:
            print("VÉRTICES DECLARADOS")
            novo_no = Vertice(v,-1)
            vertices.append(novo_no)
            

    # Determina toda a vizinhança dos vértices
    for v in vertices:
        for n in arestas:
            if v.numero in n:
                if n[0] == v.numero and n[1] not in v.adjacencia:
                    v.adjacencia.append(n[1])
                    print(v.adjacencia)
                elif n[1] == v.numero and n[0] not in v.adjacencia:
                    v.adjacencia.append(n[0])
                    print(v.adjacencia)

    print(vertices)
    # Cria e insere o vértice inicial na fila duplamente encadeada e na arvóre
    fila = deque([vertices[vertice_inicial]])
    vertices[vertice_inicial].marcado = True
    vertices[vertice_inicial].nivel_na_arvore = 1  # Vértice raiz da árvore de busca
    if window:
        vertices_enfileirados.append(vertices[vertice_inicial].numero)
    vertices_visitados.append(vertices[vertice_inicial].numero)
    
    colocar_arv(arvore, None, vertice_inicial)
    vertices[vertice_inicial].numero_pai = None
    print(vertices[vertice_inicial].nivel_na_arvore)
    # Enquanto existir a fila
    while fila:
        # Toma-se o primeiro vértice da fila
        vertice_atual = fila.popleft()

        # Para cada vizinho
        for vizinho in vertice_atual.adjacencia:
            print("Vizinho ",vizinho, "Verti adja", vertice_atual.adjacencia)
            print(vizinho)

            # Se não tiver marcado
            if not vertices[vizinho].marcado:
                # Visita a aresta
                aresta_escolhida = (vertice_atual.numero, vizinho)
                arestas_visitadas.append(aresta_escolhida)
                # Marca o vertice
                vertices[vizinho].marcado = True
                # Adiciona na fila
                fila.append(vertices[vizinho])
                if window:
                    vertices_enfileirados.append(vertices[vizinho].numero)
                vertices_visitados.append(vertices[vizinho].numero)

                arestas_pai.append(aresta_escolhida)

                # Adiciona na árvore com aresta pai
                colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero)
                vertices[vizinho].numero_pai = vertice_atual.numero
                print("Adicionando pai do ", vertices[vizinho].numero ,"Como ",vertices[vizinho].numero_pai)
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
                # Se estiver marcado e estiver na fila
                if vertices[vizinho] in fila:
                    # Visita a aresta
                    aresta_escolhida = (vertice_atual.numero, vizinho)
                    arestas_visitadas.append(aresta_escolhida)

                    #! Salvar conjunto de arestas e printar no terminal msm

                    #!Aresta irmão
                    #! Salvar os vértices que o compõe pois por meio deles poderemos apresentar o ciclo impar
                    if (vertice_atual.numero_pai == vertices[vizinho].numero_pai):
                        arestas_irmao.append(aresta_escolhida)
                        colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero, "DarkBlue")
                    #!Aresta prima
                    #! Salvar os vértices que o compõe pois por meio deles poderemos apresentar o ciclo impar
                    elif (vertice_atual.nivel_na_arvore == vertices[vizinho].nivel_na_arvore):
                        arestas_primo.append(aresta_escolhida)
                        colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero, "orange")
                    #!Aresta Tio
                    else:
                        arestas_tio.append(aresta_escolhida)
                        colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero, "DarkMagenta")
                    
                    if window:
                        atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                                            arestas_visitadas, aresta_escolhida)  # Gera imagem
                        window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
                        window['-IMAGE-'].update(f'{caminho_imagem}')
                        window['-IMAGE2-'].update(f'{"grafo/arvore.png"}')
                        window.refresh()
                        time.sleep(1)
                # Caso já esteja marcado e fora da fila não fará nada
                # Tanto que tlvz possa até tirar o else e todo bloco de código dele
                elif window:
                    atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                                        arestas_visitadas)  # Gera imagem
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window["-IMAGE2-"].update(filename="grafo/arvore.png")
                    window.refresh()
                    time.sleep(0.5)
        # Remove da fila
        

        if window:
            vertices_enfileirados.pop(0)
            window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')

    # Como se repete enquanto houver uma fila irá visitar todos os vértices sequencialmente

    if window:
        atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                            arestas_visitadas)  # Gera imagem
        window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
        window['-IMAGE-'].update(f'{caminho_imagem}')
        window["-IMAGE2-"].update(filename="grafo/arvore.png")
        window.refresh()
    # time.sleep(1)
    G_conn = isConnect(vertices_visitados,num_vertices,componentes)
    print("COMPONENTES AQUI",componentes)
    
    if (not G_conn):
        print ("O grafo é conexo")
        return False
    else:
        print ("O grafo possui as componente ",G_conn," Desconexas")
        
        buscar_em_largura( G_pgv,caminho_imagem, vertices,vertices_visitados,arestas_irmao,arestas_primo,
                          arestas_pai,arestas_tio,window, G_conn[0], arvore,componentes)
        print(vertices)
        return True
        
    



#! Para recolorir o grafo primeiro será necessário colorir ó de gray e dps pode se usar duas cores uma pra cada conjunto
#! A função pode ser feita simplesmente pintando os vértices vizinho de cor diferente dos vértices atuais
#! Enquanto o ciclo impar pode ser pintado da mesma cor

    
        
        
        

#! Mudar a direção dos dados do grafo para sua horizontal, pois os grafos tendem a ser desenhados verticalmente
#! Ocupando grande parte da janela
def interface_buscaLarg(G_pgv, matriz_adjacencia):
    global vertices_enfileirados

    #! Variáveis para guardar os dados se necessário

    caminho_imagem = caminho_imagem = "grafo/grafo.png"
    sg.theme('Reddit')

    arvore = pgv.AGraph(strict=True)

            # Layout
    arvore.layout(prog='dot')

    #O nó só está sendo adicionado para que crie a arvoré caso não exista e para que faça um nova arvoré limpa
    # Por isso a arvore é limpa logo em seguida
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
            [
            sg.Text(f'Fila: {vertices_enfileirados}', key="-TEXT-", font=("Ubuntu", 20))
            ],
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
            [sg.Text(''), sg.Text(''),sg.Text(''),sg.Text('')],
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
        sg.Push(), sg.Button('Mostrar bipartição'), sg.Button('Busca'),
        sg.Button('Sair'), sg.Push()
    ]
    ]   


    window = sg.Window('Busca em Largura', layout, resizable=True, finalize=True, auto_size_buttons=True,
                       auto_size_text=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Sair':
            print('Saindo')
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
            arvore.clear()
            zerar_cor_grafo(G_pgv)
            buscar_em_largura( G_pgv,caminho_imagem ,vertices, vertices_visitados,
                              arestas_irmao,arestas_primo, arestas_pai,arestas_tio,window, vertice_inicial, arvore)
            
            print("Saiu",vertices)
            print(arestas_primo,arestas_irmao)

            #limpa a arvore para se for feita outra busca não usar a mesma arvore

            # talvez retorna o vértice o qual a bipartição é nula
            window.Refresh()

        if event == 'Mostrar bipartição':
            print("A bipartição será mostrada recolorindo a árvore")
            isBipart(vertices, arestas_irmao, arestas_primo, arvore, G_pgv)
            arvore.clear()
            window["-IMAGE2-"].update(filename="grafo/arvoreG.png")
            window["-IMAGE-"].update(filename="grafo/G_bipart.png")
    window.close()
    return
