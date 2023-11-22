import PySimpleGUI as sg

# ! Gera o grafo e o salva como imagem
import networkx as nx
import matplotlib.pyplot as plt


def gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem, aresta_pintada=None):
    G = nx.Graph()

    # Converta a matriz de adjacência em uma lista de arestas
    arestas = []
    for i in range(len(matriz_adjacencia)):
        for j in range(len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] == 1:
                # Ajuste para iniciar a contagem dos vértices do 1
                arestas.append((i + 1, j + 1))

    G.add_edges_from(arestas)

    # Separa o grafo em componentes conectadas
    componentes = list(nx.connected_components(G))

    fig, ax = plt.subplots()

    # Desenhe as arestas e nós para cada componente separadamente usando spring_layout
    for idx, componente in enumerate(componentes):
        subgrafo = G.subgraph(componente)

        # Atribui posições iniciais diferentes para cada subgrafo
        if idx == 0:
            pos = nx.spring_layout(subgrafo, seed=42)  # Seed 42 para reprodução
        else:
            pos = nx.spring_layout(subgrafo, seed=123)  # Seed 123 para reprodução

        # Aplique um deslocamento diferente a cada subgrafo
        for k in pos:
            if idx == 0:
                pos[k][0] += idx * 2  # Ajuste o fator multiplicativo conforme necessário
            else:
                pos[k][0] -= idx * 2  # Ajuste o fator multiplicativo conforme necessário

        if aresta_pintada and aresta_pintada in subgrafo.edges():
            # Se uma aresta específica for definida, pinte essa aresta de vermelho
            nx.draw_networkx_edges(subgrafo, pos, ax=ax, edgelist=[aresta_pintada],
                                   width=2.0, edge_color='red')
            nx.draw_networkx_edges(subgrafo, pos, ax=ax,
                                   edgelist=[edge for edge in subgrafo.edges() if edge != aresta_pintada],
                                   width=1.0, alpha=0.5, edge_color='k')
        else:
            nx.draw_networkx_edges(subgrafo, pos, ax=ax, width=1.0, alpha=0.5, edge_color='k')

        # Desenhe os nós, rótulos e salve a imagem
        nx.draw_networkx_nodes(subgrafo, pos, ax=ax, node_size=700, node_color="skyblue")
        nx.draw_networkx_labels(subgrafo, pos, ax=ax, font_size=10, font_color="black", font_weight="bold")

    plt.savefig(caminho_imagem, format="png", bbox_inches="tight")
    plt.close()


# Exemplo: gerar uma imagem do grafo
matriz_adjacencia_exemplo = [
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
]

caminho_imagem_saida = "grafo/grafo.png"
aresta_escolhida = (1, 3)  # Define a aresta a ser pintada

gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem_saida, aresta_escolhida)
print(f"Imagem do grafo gerada em: {caminho_imagem_saida}")


# ! Exibir e mostrar opções doq fazer com o grafo
def main():
    # Caminho predefinido da imagem
    caminho_imagem = "grafo/grafo.png"

    # Layout da interface
    layout = [
        [sg.Image(key="-IMAGE-")],
        [sg.Push(), sg.Button('Verificar se é conexo', button_color=('white', 'DarkGreen')), sg.Push()],
        [sg.Push(), sg.Button('Aplicar busca em largura', button_color=('white', 'DarkGreen')), sg.Push()],
        [sg.Push(), sg.Button('Mostrar bipartição do grafo', button_color=('white', 'DarkGreen')), sg.Push()],
        [sg.Push(), sg.Button('Escolher outro grafo', button_color=('white', 'DarkGreen')), sg.Push()],
        [sg.Push(), sg.Button('Sair', button_color=('white', 'DarkGreen')), sg.Push()]
    ]

    # Criar a janela
    window = sg.Window("Exibir Imagem", layout, resizable=True, finalize=True)

    # Carregar a imagem inicialmente
    window["-IMAGE-"].update(filename=caminho_imagem)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Sair':
            break

    # Fechar a janela
    window.close()


if __name__ == "__main__":
    main()
