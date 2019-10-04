import statistics as stat
import csv
import math

trainingLines = 350  # Ou seja, usando as linhas 0-349


def readContent(filename: str):
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


def getGaussianParameters(samples):
    """Retorna a média e desvio padrão da média das amostras fornecidas"""
    return(stat.mean(samples), stat.stdev(samples))


def calcularDensidadeGaussiana(m, dp, x):  # Média, desvio padrão e valor amostrado
    return((1/(dp*math.sqrt(2*math.pi))) * math.exp((-1)*((x-m)**2)/(2*dp*dp)))


# ------------- CONSTRUINDO O AVALIADOR BAYESIANO -------------
fileContents = readContent('class01.csv')
# print('-----------Dados-----------\r\n')
# print(fileContents)

# Definindo as classes target e quais linhas pertencem a quais targets
targets = {}
for i in range(trainingLines):
    if(fileContents[i][len(fileContents[i])-1] not in targets.keys()):
        targets[int(fileContents[i][len(fileContents[i])-1])] = [i]
    else:
        targets[int(fileContents[i][len(fileContents[i])-1])].append(i)

# print('\r\nDicionario final:\r\n')
# print(targets)

# Calculando os atributos gaussianos para cada valor de target e cada atributo
# Os dicionários serão da forma dict[target] = [v1, v2, v3, ..., v99]
medias = {}
desviosPadrao = {}
for key in targets.keys():
    # print('Para key = ' + str(key) + ' itera-se sobre as linhas:')
    # print(targets[key])
    # print(' ')
    i = 0
    mediasPorColuna = []
    desviosPorColuna = []
    while i < len(fileContents[0]) - 1:  # iterando nas colunas. O -1 serve para excluir a coluna de targets
        amostras = []
        for numLinha in targets[key]:  # iterando nas linhas
            amostras.append(fileContents[numLinha][i])
        # print('Para o parâmetro x' + str(i) + ' as amostras são:')
        # print(amostras)
        # print(' ')
        mediaDasAmostras, desvioDasAmostras = getGaussianParameters(amostras)
        mediasPorColuna.append(mediaDasAmostras)
        desviosPorColuna.append(desvioDasAmostras)
        i += 1
    medias[key] = mediasPorColuna
    desviosPadrao[key] = desviosPorColuna

# f = open('mediasEDesvios.txt', 'w+')
# for key in medias.keys():
#     f.write('\r\nTarget = ' + str(key) + '\r\n')
#     for i in range(len(medias[key])):
#         f.write('Parâmetro x' + str(i) + ' >> Média = ' + str(medias[key][i]) + ' Variância = ' + str(desviosPadrao[key][i]) + '\r\n')

# f.close()

# ------------- TESTANDO O AVALIADOR BAYESIANO-------------
acertosNaBaseDeTreino = 0
acertosForaDaBaseDeTreino = 0
total = 0
# f = open('verossimilhanças.txt', 'w+')
for linha in range(len(fileContents)):  # len(fileContents)
    # f.write('\r\nLinha #' + str(linha) + '\r\n')
    vsPorTarget = {}
    for target in targets.keys():
        # f.write('\r\nTestando para target = ' + str(target) + '\r\n')
        vs = 1  # de verossimilhança
        i = 0
        while(i < len(medias[target])):
            DG = calcularDensidadeGaussiana(m=medias[target][i], dp=desviosPadrao[target][i], x=fileContents[linha][i])
            # f.write('Verossimilhança para o parâmetro x' + str(i) + ' = ' + str(DG) + '\r\n')
            vs = vs * DG
            i += 1
        # f.write('Verossimilhança total: ' + str(vs) + '\r\n')
        vsPorTarget[target] = vs
    # Tomando o valor de maior verossimilhança e comparando com o valor real
    targetVSMaximo = max(vsPorTarget, key=vsPorTarget.get)
    # f.write('Target de máxima verossimilhança para a linha ' + str(linha) + ': ' + str(targetVSMaximo) + '\r\n')
    # f.write('Target amostral: ' + str(int(fileContents[linha][len(fileContents[linha]) - 1])) + '\r\n')
    if(targetVSMaximo == fileContents[linha][len(fileContents[linha]) - 1]):
        if(linha < trainingLines - 1):
            acertosNaBaseDeTreino += 1
        else:
            acertosForaDaBaseDeTreino += 1
    total += 1

print('\r\nUtilizando-se ' + str(trainingLines) + ' linhas no treinamento')
print('Taxa de acertos na base de treino: ' + str(acertosNaBaseDeTreino) + '/' + str(trainingLines) + ' (' +
      str(100*(acertosNaBaseDeTreino/trainingLines)) + '%)')
print('Taxa de acertos na base de validação: ' + str(acertosForaDaBaseDeTreino) + '/' + str(total - trainingLines) + ' ('
      + str(100*(acertosForaDaBaseDeTreino/(total - trainingLines))) + '%)')
print('Taxa de acertos total: ' + str(acertosNaBaseDeTreino + acertosForaDaBaseDeTreino) + '/' + str(total) + ' ('
      + str(100*((acertosNaBaseDeTreino + acertosForaDaBaseDeTreino)/total)) + '%)')
