import PySimpleGUI as sg
import pygraphviz as pgv

def criar_grafo(matriz_adjacencia):
    G_pgv = pgv.AGraph(strict=True, directed=False, rankdir='BT')
    G_pgv.node_attr.update({'style': 'filled', 'shape': 'circle', 'width': '0.44', 'height': '0.44','fixedsize' : 'True'})
    G_pgv.edge_attr.update(penwidth='3.0')
    arestas = []

    for i in range(len(matriz_adjacencia)):
        G_pgv.add_node(i)

    for i in range(len(matriz_adjacencia)):
        for j in range(i + 1, len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] == 1:
                G_pgv.add_edge(i, j)
                arestas.append((i,j))

    G_pgv.layout(prog='neato')
    G_pgv.draw('grafo/grafo.png')
    return G_pgv

def ler_matrizes_arquivo(caminho_arquivo):
    matrizes = []
    matriz_atual = []

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()  

            if not linha:  
                if matriz_atual: 
                    matrizes.append(matriz_atual)
                    matriz_atual = []  
            else:
                elementos = [int(elemento) for elemento in linha.split()]
                matriz_atual.append(elementos)

        if matriz_atual:
            matrizes.append(matriz_atual)

    return matrizes

def interface_lerGrafo ():
    
    sg.theme('Reddit')
    caminho_do_arquivo = 'grafo/grafo.txt'
    matrizes = ler_matrizes_arquivo(caminho_do_arquivo)

    
    texto_matrizes = '\n\n'.join(['\n'.join([' '.join(map(str, linha)) for linha in matriz]) for matriz in matrizes])
    layout = [
        [sg.Multiline(default_text=texto_matrizes, size=(40, 20), autoscroll=True, key='-TEXTBOX-')],
        [sg.Text('Escolha uma matriz:'), sg.Combo(list(range(0, len(matrizes))), key='-COMBO-')],
        [sg.Button('OK')]
    ]

    window = sg.Window('Seleção de Matriz', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'OK':
            matriz_selecionada = matrizes[values['-COMBO-']]
            break

    window.close()
    
    G_pgv = criar_grafo(matriz_selecionada)
    return G_pgv, matriz_selecionada
