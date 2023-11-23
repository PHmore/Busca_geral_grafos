import PySimpleGUI as sg

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

# Leitura das matrizes
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

print(matriz_selecionada)

"""
Talvez já se deva criar a imagem do grafo nesse arquivo

Para facilitar retornar como 

grafo_exemplo = {
    'A': ['B', 'C'],
    'B': ['A', 'C'],
    'C': ['A', 'B', 'D'],
    'D': ['C']
}

"""