import PySimpleGUI as sg
import networkx as nx
import matplotlib.pyplot as plt


def ler_matrizes_arquivo(caminho_arquivo):
    matrizes = []
    matriz_atual = []

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()  # Remove espaços em branco no início e no final da linha

            if not linha:  # Verifica se a linha está em branco
                if matriz_atual:  # Verifica se a matriz atual não está vazia
                    matrizes.append(matriz_atual)
                    matriz_atual = []  # Reinicia a matriz atual
            else:
                elementos = [int(elemento) for elemento in linha.split()]
                matriz_atual.append(elementos)

        # Adiciona a última matriz, se houver alguma no final do arquivo
        if matriz_atual:
            matrizes.append(matriz_atual)

    return matrizes

def matriz_adjacencia_para_lista(matriz):
    lista_adjacencia = {}

    for i in range(len(matriz)):
        vizinhos = []
        for j in range(len(matriz[i])):
            if matriz[i][j] == 1:
                vizinhos.append(j)  # Adiciona o vértice 'j' como vizinho de 'i'
        lista_adjacencia[i] = vizinhos  # Adiciona a lista de vizinhos ao vértice 'i'

    return lista_adjacencia

def gerar_imagem_do_grafo(matriz_adjacencia, aresta_pintada=None):
    grafo = matriz_adjacencia

    # Criar um objeto do tipo Grafo não direcionado (Graph) do NetworkX
    grafo_networkx = nx.Graph()

    # Adicionar as arestas com base na lista de adjacência
    for vertice, vizinhos in grafo.items():
        for vizinho in vizinhos:
            grafo_networkx.add_edge(vertice, vizinho)

    # Adicionar vértices desconexos explicitamente
    for vertice in grafo:
        if not grafo[vertice]:  # Verifica se o vértice não possui vizinhos
            grafo_networkx.add_node(vertice)

    # Plotar o grafo com um layout circular
    pos = nx.spring_layout(grafo_networkx)  # Define a posição dos nós para um layout circular
    nx.draw(grafo_networkx, pos, with_labels=True, node_size=300, node_color='skyblue', font_weight='bold')
    plt.title('Grafo a partir de Lista de Adjacência (Layout Circular)')

    # Salvar o gráfico como uma imagem
    plt.savefig('grafo/grafo.png')  # Salva o gráfico como um arquivo PNG
    plt.close()


def interface_lerGrafo ():
    # Leitura das matrizes
    caminho_do_arquivo = 'grafo/grafo.txt'
    matrizes = ler_matrizes_arquivo(caminho_do_arquivo)

    # Criando o layout para a exibição das matrizes
    texto_matrizes = '\n\n'.join(['\n'.join([' '.join(map(str, linha)) for linha in matriz]) for matriz in matrizes])
    layout = [
        [sg.Multiline(default_text=texto_matrizes, size=(40, 20), autoscroll=True, key='-TEXTBOX-')],
        [sg.Text('Escolha uma matriz:'), sg.Combo(list(range(0, len(matrizes))), key='-COMBO-')],
        [sg.Button('OK')]
    ]

    # Criando a janela
    window = sg.Window('Seleção de Matriz', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'OK':
            matriz_selecionada = matrizes[values['-COMBO-']]
            break

    window.close()
    matriz_selecionada = matriz_adjacencia_para_lista(matriz_selecionada)
    return matriz_selecionada

"""
Talvez já se deva criar a imagem do grafo nesse arquivo

Para facilitar retornar como 

grafo_exemplo = {
    'A': ['B', 'C'],
    'B': ['A', 'C'],
    'C': ['A', 'B', 'D'],
    'D': ['C']
}

"""
