# Importa a biblioteca PySimpleGUI para criar interfaces gráficas
import PySimpleGUI as sg
# Importa funções e classes relacionadas à manipulação de grafos
from lerGrafo import interface_lerGrafo
from buscaLarg import interface_buscaLarg, buscar_em_largura
from funGrafo import *


# Função principal que controla a execução do programa
def main():
    caminho_imagem = "grafo/grafo.png"  # Caminho predefinido da imagem
    G_pgv, grafo_selecionado = interface_lerGrafo()  # Chama função de leitura do grafo através da matriz de adjacência
    sg.theme('Reddit')  # Define o tema visual da interface

    # Layout da interface gráfica
    layout = [
        [sg.Image(filename=caminho_imagem, key="-IMAGE-")],
        [sg.HSeparator()],
        [sg.Push()],
        [sg.Push(), sg.Button('Verificar se é conexo', size=(20, 1), button_color=('white', 'DarkGreen')),
         sg.Push(), sg.Button('Aplicar busca em largura', size=(20, 1), button_color=('white', 'DarkGreen')),
         sg.Push(), sg.Button('Mostrar bipartição do grafo', size=(20, 1),
                              button_color=('white', 'DarkGreen')), sg.Push()],
        [sg.Push()],
        [sg.Push(), sg.Button('Escolher outro grafo', size=(20, 1), button_color=('white', 'DarkBlue')), sg.Push()],
        [sg.Push(), sg.Button('Sair', size=(20, 1), button_color=('white', 'DarkRed')), sg.Push()]
    ]

    # Criação da janela
    window = sg.Window("Exibir Imagem", layout, resizable=True, finalize=True)
    while True:
        event, values = window.read()

        # Verifica se a janela foi fechada
        if event == sg.WIN_CLOSED:
            break

        # Verifica qual botão foi pressionado e executa a ação correspondente
        if event == 'Verificar se é conexo':
            # Inicializa listas necessárias para verificar se o grafo é conexo
            arestas_irmao = list()
            arestas_primo = list()
            vertices = list()
            vertices_visitado = list()
            arestas_pai = list()
            arestas_tio = list()
            componentes = list()

            # Faz a busca em largura através da função feita no outro arquivo
            buscar_em_largura(G_pgv, "grafo/grafo.png", vertices, vertices_visitado, arestas_irmao,
                              arestas_primo, arestas_pai, arestas_tio, None, 0, None,
                              componentes)

            # Desenha os componentes no grafo
            draw_components(G_pgv, componentes)

            # Verifica se o grafo é conexo e exibe no console
            if len(componentes) == 1:
                print("\nO GRAFO É CONEXO")
                print(componentes, "\n")
            else:
                print("\nO GRAFO É DESCONEXO E POSSUI: ", len(componentes), " COMPONENTES")
                print(componentes, "\n")

            # Atualiza a imagem do grafo na interface
            window["-IMAGE-"].update(filename="grafo/grafo.png")

        if event == 'Aplicar busca em largura':
            # Chama a interface de busca em largura e atualiza a imagem do grafo na interface
            interface_buscaLarg(G_pgv, grafo_selecionado)
            window["-IMAGE-"].update(filename="grafo/grafo.png")

        if event == 'Mostrar bipartição do grafo':
            # Inicializa listas necessárias para verificar bipartição do grafo
            arestas_irmao = list()
            arestas_primo = list()
            vertices = list()
            vertices_visitado = list()
            arestas_pai = list()
            arestas_tio = list()

            # Faz a busca em largura através da função feita no outro arquivo
            buscar_em_largura(G_pgv, "grafo/grafo.png", vertices, vertices_visitado,
                              arestas_irmao, arestas_primo, arestas_pai, arestas_tio)
            # Verifica se o grafo é bipartido e atualiza a imagem do grafo
            isBipart(vertices, arestas_irmao, arestas_primo, None, G_pgv)
            window["-IMAGE-"].update(filename="grafo/grafo.png")

        if event == 'Escolher outro grafo':
            # Chama a interface para escolher outro grafo e atualiza a imagem do grafo na interface
            G_pgv2, grafo_selecionado2 = interface_lerGrafo()
            if (G_pgv2 is not None):
                window["-IMAGE-"].update(filename=caminho_imagem)
                G_pgv = G_pgv2
                grafo_selecionado = grafo_selecionado2
                window.refresh()
            else:
                pass

        if event == 'Sair':
            break

    # Fecha a janela
    window.close()


# Verifica se o script está sendo executado como o programa principal
if __name__ == "__main__":
    main()
