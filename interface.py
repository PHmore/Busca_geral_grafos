import PySimpleGUI as sg


#! Caixa para selecionar a matriz
def criar_caixa_selecao(numero):
    layout = [
        [sg.Text('Escolha um valor:')],
        [sg.Combo(list(range(1, numero + 1)), key='combo')],
        [sg.Button('OK')]
    ]

    window = sg.Window('Interface com PySimpleGUI', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'OK':
            valor_selecionado = values['combo']
            break

    window.close()
    return valor_selecionado

# Exemplo: chama a função com o número 10
valor_selecionado = criar_caixa_selecao(10)

if valor_selecionado:
    print(f"Valor selecionado: {valor_selecionado}")
else:
    print("Nenhum valor selecionado ou janela fechada.")

#! Gera o grafo e o salva como imagem
import networkx as nx
import matplotlib.pyplot as plt

def gerar_imagem_do_grafo(matriz_adjacencia, caminho_imagem):
    G = nx.Graph()

    # Converta a matriz de adjacência em uma lista de arestas
    arestas = []
    for i in range(len(matriz_adjacencia)):
        for j in range(len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] == 1:
                # Ajuste para iniciar a contagem dos vértices do 1
                arestas.append((i + 1, j + 1))


    G.add_edges_from(arestas)

    # Use o algoritmo 'kamada_kawai_layout' para o layout
    pos = nx.kamada_kawai_layout(G)

    fig, ax = plt.subplots()

    # Desenhe as arestas com diferentes espessuras e transparências
    nx.draw_networkx_edges(G, pos, ax=ax, width=1.0, alpha=0.5, edge_color='k')

    # Desenhe os nós, rótulos e salve a imagem
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=700, node_color="skyblue")
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color="black", font_weight="bold")

    plt.savefig(caminho_imagem, format="png", bbox_inches="tight")
    plt.close()

# Exemplo: gerar uma imagem do grafo
matriz_adjacencia_exemplo = [
    [0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
]

caminho_imagem_saida = "grafo/grafo.png"
gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem_saida)
print(f"Imagem do grafo gerada em: {caminho_imagem_saida}")
    
#! Exibir e mostrar opções doq fazer com o grafo
def main():
    # Caminho predefinido da imagem
    caminho_imagem = "grafo/grafo.png"

    # Layout da interface
    layout = [
        [sg.Image(key="-IMAGE-")],
        [sg.Push(),sg.Button('Verificar se é conexo', button_color=('white', 'DarkGreen')),sg.Push()],
        [sg.Push(),sg.Button('Fazer busca em largura', button_color=('white', 'DarkGreen')),sg.Push()],
        [sg.Push(),sg.Button('Mostrar bipartição do grafo', button_color=('white', 'DarkGreen')),sg.Push()]
    ]

    # Criar a janela
    window = sg.Window("Exibir Imagem", layout, resizable=True, finalize=True)

    # Carregar a imagem inicialmente
    window["-IMAGE-"].update(filename=caminho_imagem)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

    # Fechar a janela
    window.close()

if __name__ == "__main__":
    main()
