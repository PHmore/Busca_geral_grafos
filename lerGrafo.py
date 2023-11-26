import PySimpleGUI as sg
from buscaLarg import gerar_imagem_do_grafo

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

def interface_lerGrafo ():
    # Leitura das matrizes
    sg.theme('Reddit')
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
    #matriz_selecionada = matriz_adjacencia_para_lista(matriz_selecionada)
    gerar_imagem_do_grafo(matriz_selecionada,None)
    return matriz_selecionada
