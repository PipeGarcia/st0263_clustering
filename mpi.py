import glob
import math
from random import randint

from mpi4py import MPI
from time import time
comm = MPI.COMM_WORLD

#Ruta del dataset
#pattern = "/home/csuazaca/Desktop/prueba/*.txt"
pattern = "/home/pipe/Downloads/Proyecto03/dataset/*.txt"

#Variables Globales
k = randint(8,13)
centroides = []
distAverage = []
distances = []
for i in range(glob.glob(pattern).__len__()):
    distances.append([0]*glob.glob(pattern).__len__())


clusters = []
for i in range(k):
    clusters.append([0]*glob.glob(pattern).__len__())

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
    inter = keys_1 & keys_2
    vect1 = {}
    vect2 = {}
    if inter.__len__()==0:
        return 100
    else:
        for w in inter:
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

#Halla la distancia entre Centroides y Distancias de Documentos
def distCent(filas, columnas, clusters, centroides):
    for c in range(filas):
        for j in range(columnas):
            clusters[c][j]= math.fabs(distAverage[j]-centroides[c])
    return clusters

#Halla el menor para agruparlo en el clusters correspondiente
def minor(clusters, k, filas):
    vMinor = []
    minor = 0
    aux = 0
    for j in range(filas):
        for i in range(k):
            if i==0:
                minor=clusters[i][j]
                aux=i
            elif clusters[i][j] < minor:
                minor=clusters[i][j]
                aux=i
        vMinor.insert(j, aux)
    return vMinor

#Algoritmo K-Means
def kmeans (clusters, k, filas):
    vMinor = minor(clusters, k, filas)
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

#Leer el dataset
filelist = glob.glob(pattern)

rank = comm.Get_rank()

if rank == 0:
    comm.send(distances, dest=1)
    comm.send(distances, dest=2)
    comm.send(distances, dest=3)
    comm.send(distances, dest=4)

if rank == 1:
    data1 = comm.recv(source=0)
    ds1 = distAverage
    for i in range(distances.__len__()/4):
        sum = 0
        for j in range(distances.__len__()):
            if i != j:
                distances[i][j]=similFiles(filelist[i],filelist[j])
                sum += distances[i][j]
        prom = sum / j
        ds1.insert(i, prom)
    data1 = distances[0:distances.__len__()/4]
    comm.send(data1, dest=5)
    comm.send(ds1, dest=6)

if rank == 2:
    data2 = comm.recv(source=0)
    ds2 = distAverage
    for i in range(distances.__len__()/4,distances.__len__()/2):
        sum = 0
        for j in range(distances.__len__()):
            if i != j:
                distances[i][j] = similFiles(filelist[i],filelist[j])
                sum += distances[i][j]
        prom = sum / j
        ds2.insert(i, prom)
    data2 = distances[distances.__len__()/4:distances.__len__()/2]
    comm.send(data2,dest=5)
    comm.send(ds2, dest=6)

if rank == 3:
    data3 = comm.recv(source=0)
    ds3 = distAverage
    for i in range(distances.__len__()/2,distances.__len__()/2+(distances.__len__()/4)):
        sum = 0
        for j in range(distances.__len__()):
            if i != j:
                distances[i][j] = similFiles(filelist[i],filelist[j])
                sum += distances[i][j]
        prom = sum / j
        ds3.insert(i, prom)
    data3 = distances[distances.__len__()/2:distances.__len__()/2+(distances.__len__()/4)]
    comm.send(data3,dest=5)
    comm.send(ds3, dest=6)

if rank == 4:
    data4 = comm.recv(source=0)
    ds4 = distAverage
    for i in range(distances.__len__()/2+(distances.__len__()/4),distances.__len__()):
        sum = 0
        for j in range(distances.__len__()):
            if i != j:
                distances[i][j] = similFiles(filelist[i],filelist[j])
                sum += distances[i][j]
        prom = sum / j
        ds4.insert(i, prom)
    data4 = distances[distances.__len__()/2+(distances.__len__()/4):distances.__len__()]
    comm.send(data4,dest=5)
    comm.send(ds4, dest=6)


if rank == 5:
    data1 = comm.recv(source=1)
    data2 = comm.recv(source=2)
    data3 = comm.recv(source=3)
    data4 = comm.recv(source=4)
    distances = data1+data2+data3+data4
    fn = time()
    te = fn - ini
    print "tiempo de ejecucion ", te

if rank == 6:
    ds1 = comm.recv(source=1)
    ds2 = comm.recv(source=2)
    ds3 = comm.recv(source=3)
    ds4 = comm.recv(source=4)
    distAverage = ds1+ds2+ds3+ds4

    print "distAverage ", distAverage
    for i in range(k):
        a = randint(1,distAverage.__len__()-1)
        if i == 0:
            centroides.insert(i,distAverage[a])
        else:
            while (centroides.__contains__(distAverage[a]))== True:
                a = randint(1,distAverage.__len__()-1)
            centroides.insert(i,distAverage[a])

    print "centroides ", centroides

    for i in range(20):
        print "\n"
        clusters = distCent(k,distAverage.__len__(), clusters, centroides)
        aux = centroides
        centroides = kmeans(clusters, k, distAverage.__len__())
        print "estos son los nuevos centroides"
        for i in range(k):
            print centroides[i]
        if aux == centroides:
            break
    print "\n"
    print "estas son las distancias entre documentos"
    for i in range(k):
        print clusters[i]

    vMinor = minor(clusters,k,distAverage.__len__())
    print "\n"
    print vMinor
    for i in range(k):
        print "\n"
        print "En El Cluster ", i
        for j in range(vMinor.__len__()):
            if vMinor[j]==i:
                print distAverage[j]

