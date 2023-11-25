import networkx as nx
import PySimpleGUI as sg

"""
def adicionar_filho(arvore, pai, filho, cor, nome_imagem):
    if not arvore.has_node(filho):
        arvore.add_node(filho)
    if arvore.has_node(pai):
        arvore.add_edge(pai, filho, color=cor)
    else:
        print("Erro: O nó pai não existe na árvore.")
        arvore.add_node(filho)
        print("Portanto o nó foi adicionado como filho")

    # Gera a imagem com layout top-down (de cima para baixo)
    pos = nx.nx_agraph.graphviz_layout(arvore, prog="dot", root="root", args="-Grankdir=TB")
    nx.draw(arvore, pos, with_labels=True, node_color='skyblue', font_weight='bold', node_size=500)
    nx.draw_networkx_edges(arvore, pos, width=1.0, alpha=0.5, edge_color='black')
    plt.savefig(nome_imagem, format="png", bbox_inches="tight")
    plt.close()

    return arvore
"""


def adicionar_filho(arvore, pai, filho, cor):
    if not arvore.has_node(filho):
        arvore.add_node(filho)
    if arvore.has_node(pai):
        arvore.add_edge(pai, filho, color=cor)
    else:
        print("Erro: O nó pai não existe na árvore.")
        arvore.add_node(filho)
        print("Portanto o nó foi adicionado como filho")

    # Converter para um grafo PyGraphviz
    G = nx.nx_agraph.to_agraph(arvore)

    # Configuração de tamanho para nós e arestas
    G.graph_attr.update(rankdir='TB')
    G.node_attr.update({'style': 'filled', 'shape': 'circle', 'width': '0.1', 'height': '0.1'})  # Ajuste de tamanho dos nós
    G.edge_attr.update({'penwidth': '3.0'})  # Ajuste de largura das arestas

    # Layout e geração da imagem com Graphviz
    G.layout(prog='dot')
        
    G.draw('arvore.png')
    return arvore


def arvore_test():
    # Criar um grafo não direcionado vazio (árvore)
    arvore = nx.Graph()

    # Adicionar um nó raiz (neste caso, o vértice 1)

    layout = [[sg.Image(key="-IMAGE-")],
            [sg.Text('Pai:'), sg.InputText(key='pai')],
            [sg.Text('Filho:'), sg.InputText(key='filho')],
            [sg.Text('Cor:'), sg.InputText(key='cor')],
            [sg.Button('OK')]]

    window = sg.Window('Faz arv', layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == 'OK':
            
            pai = values['pai']
            filho = values['filho']
            cor = values['cor']
            print(f"Pai: {pai}, Filho: {filho}, Cor: {cor}")
            arvore = adicionar_filho(arvore, pai, filho, cor)
            window["-IMAGE-"].update(filename="arvore.png")

arvore_test()