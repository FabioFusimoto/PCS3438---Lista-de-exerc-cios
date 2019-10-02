import statistics as stat
import csv
import numpy as np
import math


def getGaussianParameters(samples):
    """Retorna a média e desvio padrão da média das amostras fornecidas"""
    return(stat.mean(samples), stat.stdev(samples))


def readContent(filename: str, trainingLines: int):
    CSVfile = open(filename, newline='')
    fileReader = csv.reader(CSVfile, delimiter=' ', quotechar='|')
    listOfContents = []
    i = 1
    firstLine = True  # A primeira linha não precisa ser lida, porque é só o nome dos atributos
    for line in fileReader:
        if firstLine:
            firstLine = False
        else:
            rowList = []
            for row in line[0].split(','):
                rowList.append(float(row))
            listOfContents.append(rowList)
            if(i >= trainingLines):
                break
            i += 1
    return listOfContents


def calcularDensidadeGaussiana(m, dp, x):  # Média, desvio padrão e valor amostrado
    return((1/(dp*math.sqrt(2*math.pi))) * math.exp((-1)*((x-m)**2)/(2*dp*dp)))


fileContents = readContent('class01.csv', 5)
# print('-----------Dados-----------\r\n')
# print(fileContents)
# Transpondo-se os dados, fica mais fácil de se trabalhar
fileContents = np.transpose(fileContents)
# print('\r\n-----------Dados transpostos-----------\r\n')
# print(fileContents)

# Calculando as médias e desvios padrão para cada um dos atributos
medias = []
desviosPadrao = []
for i in range(len(fileContents)):
    media, desvioPadrao = getGaussianParameters(fileContents[i])
    medias.append(media)
    desviosPadrao.append(desvioPadrao)
# print('\r\nMedias: \r\n' + str(medias) + '\r\n')
# print('\r\nDesvios padrão: \r\n' + str(desviosPadrao) + '\r\n')
