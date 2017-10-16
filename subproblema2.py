import glob
import math
from random import randint
from time import time


#Ruta del dataset
#pattern = "/home/csuazaca/Desktop/prueba/*.txt"
pattern = "/home/pipe/Downloads/Proyecto03/dataset/*.txt"

#Palabras que no tienen sentido por si solas
stop_words = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself",
              "yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself",
              "they","them","their","theirs","themselves","what","which","who","whom","this","that",
              "these","those","am","is","are","was","were","be","been","being","have","has","had",
              "having","do","does","did","doing","would","should","could","ought","i'm","you're",
              "he's","she's","it's","we're","they're","i've","you've","we've","they've","i'd","you'd",
              "he'd","she'd","we'd","they'd","i'll","you'll","he'll","she'll","we'll","they'll",
              "isn't","aren't","wasn't","weren't","hasn't","haven't","hadn't","doesn't","don't",
              "didn't","won't","wouldn't","shan't","shouldn't","can't","cannot","couldn't","mustn't",
              "let's","that's","who's","what's","here's","there's","when's","where's","why's","how's",
              "a","an","the","and","but","if","or","because","as","until","while","of","at","by",
              "for","with","about","against","between","into","through","during","before","after",
              "above","below","to","from","up","down","in","out","on","off","over","under","again",
              "further","then","once","here","there","when","where","why","how","all","any","both",
              "each","few","more","most","other","some","such","no","nor","not","only","own","same",
              "so","than","too","very"]

#Tiempo inicio de ejecucion
ini = time()

#Contar numero de veces que aparece una palabra en el archivo
def countWords(filename):
    file=open(filename,"r+")
    wordCounter={}
    for word in file.read().split():
        if stop_words.__contains__(word.lower())==False:
            if word not in wordCounter:
                wordCounter[word] = 1
            else:
                wordCounter[word] += 1
        file.close()
    return wordCounter

#Compara que tan similares son 2 documentos
def similFiles(file1, file2):
    countWords1 = countWords(file1)
    countWords2 = countWords(file2)
    keys_1 = set(countWords1.keys())
    keys_2 = set(countWords2.keys())
    intersection = keys_1 & keys_2
    vect1 = {}
    vect2 = {}
    if intersection.__len__()==0:
        return 100
    else:
        for w in intersection:
            vect1[w] = countWords1[w]
            vect2[w] = countWords2[w]
        return euclideanDistance(vect1, vect2)

#Realiza la distancia euclidiana entre 2 documentos
def euclideanDistance(vect1, vect2):
    sum = 0
    for cont in vect1:
        sum += math.pow((vect1[cont] - vect2[cont]), 2)
    sum = math.sqrt(sum)
    return sum

#Halla el menor para agruparlo en el clusters correspondiente
def minor(Clusters, k, filas):
    vMinor = []
    minor = 0
    aux = 0
    for j in range(filas):
        for i in range(k):
            if i==0:
                minor=Clusters[i][j]
                aux=i
            elif Clusters[i][j] < minor:
                minor=Clusters[i][j]
                aux=i
        vMinor.insert(j, aux)
    return vMinor

#Algoritmo K-Means
def kmeans (Clusters, k, filas):
    vMinor = minor(Clusters, k, filas)
    centroides = []
    for i in range(k):
        sum = 0
        for j in range(vMinor.__len__()):
            if vMinor[j]==i:
                sum += distAverage[j]
        if vMinor.count(i) !=0:
            prom = sum / vMinor.count(i)
            centroides.insert(i, prom)
        else:
            centroides.insert(i, 0)
    return centroides

#Halla la distancia entre Centroides y Distancias de Documentos
def distCent(filas, columnas, Clusters, centroides):
    for c in range(filas):
        for j in range(columnas):
            Clusters[c][j]= math.fabs(distAverage[j]-centroides[c])
    return Clusters


#Leer el dataset
filelist = glob.glob(pattern)
distances = []
centroides = []

#Crear la distancias para almacenar las distancias entre documentos
for k in range (filelist.__len__()):
    distances.append([0]*filelist.__len__())

#Llenar la matriz de distancias con las distancias.
for i in range(distances.__len__()):
    for j in range(distances.__len__()):
        if i != j:
            distances[i][j]=similFiles(filelist[i],filelist[j])

for i in range(distances.__len__()):
    print distances[i]



distAverage = []

#Crear Dataset de Promedios por cada fila de la matriz de distancias
for i in range(distances.__len__()):
    sum = 0
    for j in range(distances.__len__()):
        sum += distances[i][j]
    prom = sum / j
    distAverage.insert(i,prom)

print "Distancia Promedio"
print distAverage

#Hallar aleatoriamente los centroides iniciales
k = 3
for i in range(k):
        a = randint(1,distAverage.__len__()-1)
        if i == 0:
            centroides.insert(i,distAverage[a])
        else:
            while (centroides.__contains__(distAverage[a]))== True:
                a = randint(1,distAverage.__len__()-1)
            centroides.insert(i,distAverage[a])

#Crear matriz para las distancias entre los promedios de distancias y centroides
Clusters = []
for i in range (k):
    Clusters.append([0]*filelist.__len__())


print "estos son los centroides iniciales"
for i in range(k):
    print centroides[i]

#en este caso las iteraciones para hallar convergencia son 20
for i in range(20):
    print "\n"
    Clusters = distCent(k,distAverage.__len__(), Clusters, centroides)
    aux = centroides
    centroides = kmeans(Clusters, k, distAverage.__len__())
    print "estos son los nuevos centroidesroides"
    for i in range(k):
        print centroides[i]
    if aux == centroides:
        break

print "\n"
print "estas son las distancias entre documentos"
for i in range(k):
    print Clusters[i]

vMinor = minor(Clusters,k,distAverage.__len__())
print "\n"
print vMinor
for i in range(k):
    print "\n"
    print "En El Cluster ", i
    for j in range(vMinor.__len__()):
        if vMinor[j]==i:
            print distAverage[j]

fn = time()
te = fn - ini
print "tiempo de ejecucion ", te
