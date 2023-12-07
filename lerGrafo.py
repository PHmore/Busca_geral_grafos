import PySimpleGUI as sg
import pygraphviz as pgv


# Função para criar o grafo usando PyGraphviz
def criar_grafo(matriz_adjacencia):
    # Inicialização do grafo PyGraphviz
    G_pgv = pgv.AGraph(strict=True, directed=False, rankdir='BT')
    G_pgv.node_attr.update(
        {'style': 'filled', 'shape': 'circle', 'width': '0.44', 'height': '0.44', 'fixedsize': 'True'})
    G_pgv.edge_attr.update(penwidth='3.0')
    arestas = []

    # Adiciona nós ao grafo com base no tamanho da matriz
    for i in range(len(matriz_adjacencia)):
        G_pgv.add_node(i)

    # Adiciona arestas ao grafo com base na matriz de adjacência
    for i in range(len(matriz_adjacencia)):
        for j in range(i + 1, len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] == 1:
                G_pgv.add_edge(i, j)
                arestas.append((i, j))

    # Define o layout do grafo e gera a imagem
    G_pgv.layout(prog='neato')
    G_pgv.draw('grafo/grafo.png')
    return G_pgv


# Função para ler matrizes de um arquivo
def ler_matrizes_arquivo(caminho_arquivo):
    matrizes = []
    matriz_atual = []

    # Lê as matrizes do arquivo, onde uma linha em branco indica o fim de uma matriz
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


# Função para criar a interface de seleção de matriz
def interface_lerGrafo():
    sg.theme('Reddit')
    caminho_do_arquivo = 'grafo/grafo.txt'
    matrizes = ler_matrizes_arquivo(caminho_do_arquivo)

    # Formata o texto exibido na janela da interface
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
            return None, None

        if event == 'OK':
            try:
                matriz_selecionada = matrizes[values['-COMBO-']]
            except:
                matriz_selecionada = matrizes[0]
            break

    window.close()

    G_pgv = criar_grafo(matriz_selecionada)
    return G_pgv, matriz_selecionada
