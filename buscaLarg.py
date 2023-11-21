#Aqui será feita a busca em largura OBS: A busca deve ser realizada mesmo que o usuário selecione a opção 3

"""
6 – Caso o usuário selecione a opção “2” o programa deve perguntar: “Qual será o vértice raiz da
busca?” e apresentar a listagem dos vértices candidatos; Na sequência deve-se ser apresentada a
árvore de busca em largura e apresentar pelo menos o ponto em que foi identificado que o grafo não
seria Bipartido, no caso de o grafo não ser;

** O algoritmo de reconhecimento deve utilizar a Busca em Largura tal como foi estudada em sala
de aula;
*** Os conjuntos de arestas geradas pela busca em largura devem ser apresentados.
"""

import PySimpleGUI as sg

#! Gera o grafo e o salva como imagem
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
print(f"Imagem do grafo gerada em: {caminho_imagem_saida}")
x = 1

import PySimpleGUI as sg


caminho_imagem = "grafo/grafo.png"
sg.theme ('Reddit')


# Exemplo: criar uma fila com tamanho variável de 8
tamanho = 8

layout = [[sg.Image(key="-IMAGE-")],
          [sg.Button('Busca')],
          [sg.Graph(canvas_size=(400, 50), graph_bottom_left=(0, 0), graph_top_right=(400, 50), key='graph')]]


window = sg.Window('Janela está aberta',layout,resizable=True, finalize=True)

graph = window['graph']
largura_celula = 400 // tamanho  # Divide a largura pelo número de elementos na fila
altura_celula = 50

for i in range(tamanho):
    graph.draw_rectangle((i * largura_celula, 0), (i * largura_celula + largura_celula, altura_celula),
                         line_color='black')

while True:
    window["-IMAGE-"].update(filename=caminho_imagem)
    event, values = window.read()
    print(event, values)
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Read':
        window['-IN-'].update('')
    
    if event == 'Busca':
        print("Será buscado" , x)
        aresta_escolhida = (x, 3)  # Define a aresta a ser pintada
        gerar_imagem_do_grafo(matriz_adjacencia_exemplo, caminho_imagem_saida, aresta_escolhida)
        x=x+1

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