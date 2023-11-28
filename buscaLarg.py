# Aqui será feita a busca em largura OBS: A busca deve ser realizada mesmo que o usuário selecione a opção 3

#!ERROS
# Entender pq o grafo 8 não está realizando a 2 busca

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
from Vertice import Vertice
from lerGrafo import *
from collections import deque
import networkx as nx
import pygraphviz as pgv


# ! Talvez seja interessante deixa escolher qualquer vértice pois se o grafo for desconexo ele gera duas arvores
# ! Esse mesmo fator pode ser usado para mostrar as componentes desconexas por meio de arvores e

# !usando set para cada componente e comporando a quantidade de vértices encontrados com a quantidade de nós totais

# ! Tentar fazer com que sair no meio do programa não mostre a tela de morte



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
    #Retornará os 3 principais vértices
    #dados_tabela = dados_tabela[:3]
    return dados_tabela

def vert_inicial(grafo):
    sg.theme('Reddit')
    # Dados da tabela (vértices e graus)
    dados_tabela = calcular_grau_vertice(grafo)

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

def criar_grafo(matriz_adjacencia):
    G_pgv = pgv.AGraph(strict=True, directed=False, rankdir='BT')
    G_pgv.node_attr.update({'style': 'filled', 'shape': 'circle', 'width': '0.44', 'height': '0.44','fixedsize' : 'True'})
    arestas = []

    for i in range(len(matriz_adjacencia)):
        G_pgv.add_node(i)

    for i in range(len(matriz_adjacencia)):
        for j in range(i + 1, len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] == 1:
                G_pgv.add_edge(i, j)
                arestas.append((i,j))
                print("arestas na função: ",arestas)

    G_pgv.layout(prog='neato')
    G_pgv.draw('grafo/grafo.png')
    return G_pgv

#! Mudar para receber o grafo e fazer as mudanças
def atualizar_grafo(G_pgv = None, no_atual=None, no_visitados=None, arestas_visitadas=None,
                          aresta_pintada=None):
    
    def draw_edges(edges, color, width, G = G_pgv):
        for edge in edges:
            pgv_edge = G.get_edge(*edge)
            pgv_edge.attr['color'] = color
            pgv_edge.attr['penwidth'] = width

    # Se houverem arestas visitadas, desenha-as em vermelho
    if arestas_visitadas:
        draw_edges(arestas_visitadas, 'red', 2.0)

    # Se houver uma aresta pintada, desenha-a em verde
    if aresta_pintada:
        draw_edges([aresta_pintada], 'green', 2.0)

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

def colocar_arv (arvore, pai, filho, cor = "black"):
    #! Aresta especial
    if arvore.has_node(pai) and arvore.has_node(filho):
        arvore.add_edge(pai, filho, color=cor, constraint = False)
    #! Aresta de arvore
    elif not arvore.has_node(filho) and arvore.has_node(pai):
        arvore.add_node(filho)
        arvore.add_edge(pai, filho, color=cor)
    #! Nó inicial
    else:
        arvore.add_node(filho)


    # Converter para um grafo PyGraphviz
    G = nx.nx_agraph.to_agraph(arvore)

    # Configuração de tamanho para nós e arestas
    G.graph_attr.update(rankdir='TB')
    G.node_attr.update({'style': 'filled', 'shape': 'circle', 'width': '0.3', 'height': '0.3','fixedsize' : 'True' ,'color':'lightblue'})  # Ajuste de tamanho dos nós
    G.edge_attr.update({'penwidth': '3.0'})  # Ajuste de largura das arestas

    # Layout e geração da imagem com Graphviz
    G.layout(prog='dot')
        
    G.draw('grafo/arvore.png')
    return arvore

def buscar_em_largura(window,G_pgv,caminho_imagem, vertices_visitados, vertice_inicial=None,arvore = None, ):
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
                vertices_enfileirados.append(vertices[vizinho].numero)
                vertices_visitados.append(vertices[vizinho].numero)

                arestas_pai.append(aresta_escolhida)

                # Adiciona na árvore com aresta pai
                colocar_arv(arvore, vertice_atual.numero, vertices[vizinho].numero)
                vertices[vizinho].numero_pai = vertice_atual.numero
                print("Adicionando pai do ", vertices[vizinho].numero ,"Como ",vertices[vizinho].numero_pai)
                vertices[vizinho].nivel_na_arvore = vertice_atual.nivel_na_arvore + 1

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

                    atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                                          arestas_visitadas, aresta_escolhida)  # Gera imagem
                    window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window['-IMAGE2-'].update(f'{"grafo/arvore.png"}')
                    window.refresh()
                    time.sleep(1)
                # Caso já esteja marcado e fora da fila não fará nada
                # Tanto que tlvz possa até tirar o else e todo bloco de código dele
                else:
                    atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                                          arestas_visitadas)  # Gera imagem
                    window['-IMAGE-'].update(f'{caminho_imagem}')
                    window["-IMAGE2-"].update(filename="grafo/arvore.png")
                    window.refresh()
                    time.sleep(0.5)
        # Remove da fila
        vertices_enfileirados.pop(0)
        window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')

    # Como se repete enquanto houver uma fila irá visitar todos os vértices sequencialmente

    atualizar_grafo(G_pgv, vertice_atual.numero, vertices_visitados,
                          arestas_visitadas)  # Gera imagem
    window["-TEXT-"].update(f'Fila: {vertices_enfileirados}')
    window['-IMAGE-'].update(f'{caminho_imagem}')
    window["-IMAGE2-"].update(filename="grafo/arvore.png")
    window.refresh()
    # time.sleep(1)
    G_conn = isConnect(vertices_visitados,num_vertices)
    
    if (not G_conn):
        print ("O grafo é conexo")
    else:
        print ("O grafo possui as componente ",G_conn," Desconexas")
        buscar_em_largura(window, G_pgv,caminho_imagem, vertices_visitados, G_conn[0], arvore)
    print(vertices)
        
    

def isConnect (vertices_comp,vertices_totais):

    print("Todas vert",vertices_totais,vertices_comp)

    vertices_comp = set (vertices_comp)
    vertices_totais = set (vertices_totais)

    resultado = vertices_totais - vertices_comp 
    print ("Resultado", resultado)
    print(vertices_totais, vertices_comp)
    return list(resultado)

#! Essa função pode recolorir a árvore ou o grafo ou ambos, acho interessante recolorir ambos
#! Para recolorir o grafo primeiro será necessário colorir ó de gray e dps pode se usar duas cores uma pra cada conjunto
#! A função pode ser feita simplesmente pintando os vértices vizinho de cor diferente dos vértices atuais
#! Enquanto o ciclo impar pode ser pintado da mesma cor
def isBipart (arvore, G_pgv = None):
    def draw_nodes(nodes, color, G = G_pgv):
            for node in nodes:
                pgv_node = G.get_node(node)
                pgv_node.attr['color'] = color
    
    if arestas_irmao or arestas_primo:
        print("O grafo não é bipartido e um ciclo ímpar será pintado")
        print(vertices)
        arestas_special = list()
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
    
        print("Passando pelo for nenhum vértice é igual: ",arestas_special[0][0],arestas_special[0][1])
        ciclo_impar.append(verticeA.numero)
        ciclo_impar.append(verticeB.numero)
        while verticeA.numero_pai != verticeB.numero_pai:
            print(ciclo_impar)
            print("Vertice A numero: ",verticeA.numero)
            print("Vertice B numero: ",verticeB.numero)
            for v in vertices:
                if v.numero == verticeA.numero_pai:
                    verticeA = v
                    break
            for v in vertices:
                if v.numero == verticeB.numero_pai:
                    verticeB = v
                    break
            print("Vertice A numero: ",verticeA.numero)
            print("Vertice B numero: ",verticeB.numero)
            ciclo_impar.append(verticeA.numero)
            ciclo_impar.append(verticeB.numero)
        ciclo_impar.append(verticeA.numero_pai)
        print("Pai: ",verticeA.numero_pai, verticeB.numero_pai)
            

        print(ciclo_impar)
        
        draw_nodes(ciclo_impar,'yellow')
        verticeA = None
        verticeB = None
        ciclo_impar.clear()
        arestas_special.clear()


    else:
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
        draw_nodes(groupA,'yellow',G_pgv)
        draw_nodes(groupB,'pink',G_pgv)
    G_pgv.draw('grafo/G_bipart.png')
        
        
        

#! Mudar a direção dos dados do grafo para sua horizontal, pois os grafos tendem a ser desenhados verticalmente
#! Ocupando grande parte da janela
def interface_buscaLarg(grafo):
    global vertices_enfileirados

    #! Variáveis para guardar os dados se necessário
    global arestas_pai
    global arestas_primo
    global arestas_tio
    global arestas_irmao
    global vertices
    global componentes

    matriz_adjacencia = grafo

    caminho_imagem = caminho_imagem = "grafo/grafo.png"
    sg.theme('Reddit')

    """
    lista = matriz_adjacencia_para_lista(matriz_adjacencia)
    calcular_grau(lista)

    for vertice, grau in lista.items():
        print(f'O vértice {vertice} possui grau {grau}')
    """

    arvore = nx.Graph()
    colocar_arv(arvore,None,0)
    arvore.clear()

    componentes = 0

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
            G_pgv = criar_grafo(matriz_adjacencia)
            buscar_em_largura(window, G_pgv,caminho_imagem , vertices_visitados, vertice_inicial, arvore)
            
            print("Saiu",vertices)
            print(arestas_primo,arestas_irmao)

            #limpa a arvore para se for feita outra busca não usar a mesma arvore
            arvore.clear()
            # talvez retorna o vértice o qual a bipartição é nula
            window.Refresh()
        if event == 'Mostrar bipartição':
            print("A bipartição será mostrada recolorindo a árvore")
            isBipart(arvore,G_pgv)
            window["-IMAGE-"].update(filename="grafo/G_bipart.png")
    window.close()
    return