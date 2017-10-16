import glob
import math
import operator

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

#Leer el dataset
filelist = glob.glob(pattern)
distances = []

#Crear la matriz para almacenar las distancias entre documentos
for k in range (filelist.__len__()):
    distances.append([0]*filelist.__len__())

#Llenar la matriz de distancias con las distancias.
for i in range(distances.__len__()):
    for j in range(distances.__len__()):
        if i != j:
            distances[i][j]=similFiles(filelist[i],filelist[j])

for i in range(distances.__len__()):
    print distances[i]
