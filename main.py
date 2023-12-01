import PySimpleGUI as sg

# ! Gera o grafo e o salva como imagem
from lerGrafo import interface_lerGrafo
from buscaLarg import interface_buscaLarg, buscar_em_largura
from funGrafo import *


# ! Exibir e mostrar opções doq fazer com o grafo

#! Resolver problema do carregamento inicial de imagens e quando não existem imagens
#! Necessário rever o uso de vertices infileirados pois o mesmo precisa existir

#? Para encontrar bipartição no grafo apartir de uma aresta especial
#? Pode se pegar igualar o nível dos vértices e subir a árvore até a aresta a,b possuirem o mesmo pai
#? Fazer esse processo recolorindo os nós pelo caminho resultará em teoria em um ciclo impar
#? Portanto tentar implementar posteriomente

def main():
    # Caminho predefinido da imagem
    caminho_imagem = "grafo/grafo.png"
    G_pgv, grafo_selecionado = interface_lerGrafo()
    sg.theme('Reddit')

    # Layout da interface
    layout = [
        [sg.Image(filename=caminho_imagem,key="-IMAGE-")],
        [sg.HSeparator()],
        [sg.Push()],
        [sg.Push(), sg.Button('Verificar se é conexo',size=(20, 1), button_color=('white', 'DarkGreen')),
         sg.Push(), sg.Button('Aplicar busca em largura',size=(20, 1), button_color=('white', 'DarkGreen')),
         sg.Push(), sg.Button('Mostrar bipartição do grafo',size=(20, 1),
                              button_color=('white', 'DarkGreen')), sg.Push()],
        [sg.Push()],
        [sg.Push(), sg.Button('Escolher outro grafo', size=(20, 1), button_color=('white', 'DarkBlue')), sg.Push()],
        [sg.Push(), sg.Button('Sair', size=(20, 1), button_color=('white', 'DarkRed')), sg.Push()]
    ]

    # Criar a janela
    window = sg.Window("Exibir Imagem", layout, resizable=True, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        
        if event == 'Verificar se é conexo':
            print("Será feita " ,event)
            #G_connect_interface(grafo_selecionado)
            arestas_irmao = list()
            arestas_primo = list()
            vertices = list()
            vertices_visitado= list()
            arestas_pai = list()
            arestas_tio = list()
            if buscar_em_largura(G_pgv,"grafo/grafo.png",vertices,vertices_visitado,arestas_irmao,arestas_primo,arestas_pai,arestas_tio):
                print ("O grafo é desconexo")

        if event == 'Aplicar busca em largura':

            interface_buscaLarg(G_pgv, grafo_selecionado)

        if event == 'Mostrar bipartição do grafo':
            print("Será feita")

        if event == 'Escolher outro grafo':
            G_pgv, grafo_selecionado = interface_lerGrafo()
            window["-IMAGE-"].update(filename=caminho_imagem)
            window.refresh()

        if event == 'Sair':
            break

    # Fechar a janela
    window.close()


if __name__ == "__main__":
    main()
