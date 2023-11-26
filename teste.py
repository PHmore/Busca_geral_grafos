import pygraphviz as pgv

def criar_grafo():
    # Criando um novo gráfico direcionado
    G = pgv.AGraph(strict=True, directed=True)

    # Adicionando nós ao gráfico com diferentes tamanhos
    G.add_node('A', width=0.2, height=0.2, fixedsize = True)  # Nó 'A' com tamanho 0.5
    G.add_node('B', width=1.0, height=1.0)  # Nó 'B' com tamanho 1.0
    G.add_node('C', width=1.5, height=1.5)  # Nó 'C' com tamanho 1.5

    # Adicionando arestas (conexões) entre os nós
    G.add_edge('A', 'B')
    G.add_edge('B', 'C')
    G.add_edge('C', 'A')

    return G

# Criando o gráfico
grafo = criar_grafo()

# Visualizando o gráfico (para um ambiente de notebook, por exemplo)
grafo.draw('grafo.png', prog='dot')
