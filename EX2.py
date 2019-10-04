import csv
import sys
import math


def lerArquivoCSV(filename: str):
    CSVfile = open(filename, newline='')
    fileReader = csv.reader(CSVfile, delimiter=' ', quotechar='|')
    listOfContents = []
    firstLine = True  # A primeira linha não precisa ser lida, porque é só o nome dos atributos
    for line in fileReader:
        if firstLine:
            firstLine = False
        else:
            rowList = []
            for row in line[0].split(','):
                rowList.append(float(row))
            listOfContents.append(rowList)
    return listOfContents


def calcularDistanciaEuclidiana(ponto1, ponto2):
    if(len(ponto1) != len(ponto2)):
        print('Dimensões diferentes')
        sys.exit()

    somaQuadratica = 0
    for(coordenada1, coordenada2) in zip(ponto1, ponto2):
        somaQuadratica += (coordenada1 - coordenada2) ** 2

    return(math.sqrt(somaQuadratica))


# -------- LENDO DO BANCO DE DADOS ---------
dados = lerArquivoCSV(filename='class02.csv')
# txt = open('dadosLidos.txt', 'w+')
# txt.write(str(dados))
# txt.close()

# -------- RODANDO O CLASSIFICADOR ---------
k = 10
qtdPastas = 5
acertosNaPasta = 0
acertosTotais = 0
testesTotais = 0
usarPonderacaoPorDistancia = False

ponderar = input('Usar ponderação por distância? s/S -> Usar / Outro caractere -> Não usar\r\n')
if(ponderar == 's' or ponderar == 'S'):
    usarPonderacaoPorDistancia = True

# testePastas = open('testePastas.txt', 'w+')
for numPasta in range(qtdPastas):
    # testePastas.write('\r\nPasta #' + str(numPasta) + '\r\nLinhas:')
    # print('Usando a pasta #' + str(numPasta) + ' como validação')
    acertosNaPasta = 0
    for linhaValidacao in range(int((numPasta)*(len(dados)/qtdPastas)), int((numPasta + 1)*(len(dados)/qtdPastas))):
        # Esse if inclui apenas as linhas da pasta de validação
        # print('Validando com a linha #' + str(linhaValidacao))
        distancias = []  # distancias[i] = (distanciaEuclidiana, numLinha)
        NN = {}  # NN[target] = contagemDeVizinhos
        for linhaTreino in range(len(dados)):
            if(linhaTreino not in range(int((numPasta)*(len(dados)/qtdPastas)), int((numPasta + 1)*(len(dados)/qtdPastas)))):
                # Esse if exclui as linhas da pasta de validação
                # testePastas.write(str(linha) + ', ')
                # Exclui-se a última linha porque esta contém o valor target
                distancias.append([calcularDistanciaEuclidiana(dados[linhaTreino][0:(len(dados) - 1)],
                                                               dados[linhaValidacao][0:(len(dados) - 1)]), linhaTreino])
        # Ordena-se as distâncias em ordem crescente
        distancias.sort(key=lambda tup: tup[0])
        qtdNN = 0  # Quantidade de vizinhos mais próximos analisados
        while(qtdNN < k):
            if dados[distancias[qtdNN][1]][len(dados[linhaTreino]) - 1] not in NN.keys():
                if(not usarPonderacaoPorDistancia):
                    NN[dados[distancias[qtdNN][1]][len(dados[linhaTreino]) - 1]] = 1
                else:
                    NN[dados[distancias[qtdNN][1]][len(dados[linhaTreino]) - 1]] = 1/(distancias[qtdNN][0])
            else:
                if(not usarPonderacaoPorDistancia):
                    NN[dados[distancias[qtdNN][1]][len(dados[linhaTreino]) - 1]] += 1
                else:
                    NN[dados[distancias[qtdNN][1]][len(dados[linhaTreino]) - 1]] += 1/(distancias[qtdNN][0])
            qtdNN += 1
        # Conta-se qual é o vizinho mais próximo baseado nos votos e vê se o resultado está correto
        vizinhoMaisProximo = max(NN, key=NN.get)
        if(vizinhoMaisProximo == dados[linhaValidacao][len(dados[linhaValidacao]) - 1]):
            acertosNaPasta += 1
        testesTotais += 1
    print('Total de acertos para a pasta #' + str(numPasta + 1) + ': ' + str(acertosNaPasta) + '/' + str(int(len(dados)/qtdPastas)) + '(' +
          '% 5.3f' % (100*acertosNaPasta/int(len(dados)/qtdPastas)) + '%)')
    acertosTotais += acertosNaPasta

print('Acertos totais: ' + str(acertosTotais) + '/' + str(len(dados)) + '(' +
      '% 5.3f' % (100*acertosTotais/len(dados)) + '%)')
# testePastas.close()
