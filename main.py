import PySimpleGUI as sg

# ! Gera o grafo e o salva como imagem
from lerGrafo import interface_lerGrafo
from lerGrafo import gerar_imagem_do_grafo
from buscaLarg import interface_buscaLarg

# ! Exibir e mostrar opções doq fazer com o grafo

#! Resolver problema do carregamento inicial de imagens e quando não existem imagens
def main():
    # Caminho predefinido da imagem
    caminho_imagem = "grafo/grafo.png"
    grafo_selecionado = interface_lerGrafo()

    # Layout da interface
    layout = [
        [sg.Image(filename=caminho_imagem,key="-IMAGE-")],
        [sg.Push(), sg.Button('Verificar se é conexo',size=(20, 1), button_color=('white', 'DarkGreen')),
         sg.Push(), sg.Button('Aplicar busca em largura',size=(20, 1), button_color=('white', 'DarkGreen')),
         sg.Push(), sg.Button('Mostrar bipartição do grafo',size=(20, 1),
                              button_color=('white', 'DarkGreen')), sg.Push()],
        [sg.Push()],
        [sg.Push(), sg.Button('Escolher outro grafo',size=(20, 1), button_color=('white', 'DarkBlue')), sg.Push()],
        [sg.Push(), sg.Button('Sair',size=(20, 1), button_color=('white', 'DarkRed')), sg.Push()]
    ]

    # Criar a janela
    window = sg.Window("Exibir Imagem", layout, resizable=True, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        
        if event == 'Verificar se é conexo':
            print("Será feita " ,event)

        if event == 'Aplicar busca em largura':
            interface_buscaLarg(grafo_selecionado)

        if event == 'Mostrar bipartição do grafo':
            print("Será feita " ,event)

        if event == 'Escolher outro grafo':
            #mudar grafo
            grafo_selecionado = interface_lerGrafo()
            window["-IMAGE-"].update(filename=caminho_imagem)
            window.refresh()

        if event == 'Sair':
            break

    # Fechar a janela
    window.close()


if __name__ == "__main__":
    main()
