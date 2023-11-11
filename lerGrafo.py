#Aqui teremos a leitura do arquivo de grafos e será separado em diferentes matrizes

# 2.1 – O arquivo “grafo.txt” pode conter várias matrizes de adjacências, de vários grafos, separadas
# por uma linha em branco. Dessa forma, logo depois de ler o arquivo o programa deve informar
# quantas matrizes foram carregadas e qual delas o usuário deseja manipular #

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

# Exemplo de uso
caminho_do_arquivo = 'grafo/grafo.txt'
matrizes = ler_matrizes_arquivo(caminho_do_arquivo)

# Imprime as matrizes
for i, matriz in enumerate(matrizes, start=1):
    print(f"Matriz {i}:")
    for linha in matriz:
        print(linha)
    print()

grafoNum = input(f"Selecione um grafo de 1 a {len(matrizes)}: ")

# Acesse a matriz 2 (índice 1 na lista)
grafoNum = matrizes[int(grafoNum) - 1]

grafoEsc = []

# Imprima a matriz 2
print("Matriz 2:")
for linha in grafoNum:
    grafoEsc.append(linha)
    print(linha)

print("Matriz escolhida:")
for linha in grafoEsc:
    print(linha)

