import PySimpleGUI as sg

#importação usada em busca em largura
from Vertice import Vertice
#from buscaLarg import interface_buscaLarg

# Aqui estarão as outras funções

# Apresentar o grafo visualmente acima da opções

# Verificar se é conexo

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

def isConnect (vertices_encontrados,vertices_totais,componente = []):

    print("Todas vert",vertices_totais,vertices_encontrados)

    vertices_encontrados = set (vertices_encontrados)
    vertices_totais = set (vertices_totais)
    nova_componente = list(vertices_encontrados - set(sum(componente, [])))
    componente.append(nova_componente)
    resultado = vertices_totais - vertices_encontrados 
    print ("Resultado", resultado)
    print(vertices_totais, vertices_encontrados)
    return list(resultado)

def isBipart (vertices,arestas_irmao, arestas_primo,arvore = None, G_pgv = None):

    def draw_bipart(nodes, color, G_pgv = None, arvore = None, arestas = None):
            for node in nodes:
                if G_pgv:
                    pgv_node = G_pgv.get_node(node)
                    pgv_node.attr['color'] = color
                    if arestas:
                        for aresta in arestas:
                            pgv_edge = G_pgv.get_edge(*aresta)
                            pgv_edge.attr['color'] = color
                    G_pgv.draw('grafo/G_bipart.png')
                if arvore:
                    pgv_node = arvore.get_node(node)
                    pgv_node.attr['color'] = color

        # Layout
                    arvore.draw('grafo/arvoreG.png')
    
    if arestas_irmao or arestas_primo:
        print("O grafo não é bipartido e um ciclo ímpar será pintado")
        print(vertices)
        arestas_special = list()
        ciclo_impar_arestas = list ()
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
        ciclo_impar_arestas.append(arestas_special[0])
        ciclo_impar.append(verticeA.numero)
        ciclo_impar.append(verticeB.numero)
        while verticeA.numero_pai != verticeB.numero_pai:
            print(ciclo_impar)
            print("Vertice A numero: ",verticeA.numero)
            print("Vertice B numero: ",verticeB.numero)
            for v in vertices:
                if v.numero == verticeA.numero_pai:
                    ciclo_impar_arestas.append((verticeA.numero,v.numero))
                    verticeA = v
                    break
            for v in vertices:
                if v.numero == verticeB.numero_pai:
                    ciclo_impar_arestas.append((verticeB.numero,v.numero))
                    verticeB = v
                    break
            print("Vertice A numero: ",verticeA.numero)
            print("Vertice B numero: ",verticeB.numero)
            ciclo_impar.append(verticeA.numero)
            ciclo_impar.append(verticeB.numero)
        ciclo_impar.append(verticeA.numero_pai)
        ciclo_impar_arestas.append((verticeB.numero,verticeA.numero_pai))
        ciclo_impar_arestas.append((verticeA.numero,verticeA.numero_pai))
        print("Pai: ",verticeA.numero_pai, verticeB.numero_pai)
            

        print(ciclo_impar)
        print(arestas_special)
        print(ciclo_impar_arestas)
        
        draw_bipart(ciclo_impar,'yellow',G_pgv, arvore,ciclo_impar_arestas)
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
        draw_bipart(groupA,'yellow',G_pgv,arvore)
        draw_bipart(groupB,'pink',G_pgv,arvore)

def draw_components(G_pgv,componentes):
    colors = ['green','blue','pink','orange','violet']


    def draw_nodes(nodes, color, G = G_pgv):
        for node in nodes:
            pgv_node = G.get_node(node)
            pgv_node.attr['color'] = color

    #i = 0

    for componente in componentes:
        #print("Componente única",componente)
        draw_nodes(componente,colors.pop(),G_pgv)

        #draw_nodes(componente,colors[i],G_pgv)
        #i+=1;
        
    
    G_pgv.draw('grafo/grafo.png')

