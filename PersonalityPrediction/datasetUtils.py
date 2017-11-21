from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import os

def parseFastText(path):
    data = {}
    dataset = open(path, "r", encoding="utf8")
    [num_words, embedding_size] = dataset.readline().split(" ")
    i=1
    print("Reading dataset file...")
    for line in dataset:
        [word, embedding] = line[:-1].split(" ",1)
        data[word] = embedding
        percentage = round( (100*(i/int(num_words))),1 )
        i += 1
        print("  %.1f%% complete" %percentage, end="\r")
    print("\n")
    dataset.close()
    return data

def loadEmbeddingsDataset(path):
    return KeyedVectors.load_word2vec_format(path, binary=True)

def readMyPersonality():
    data = []
    for line in open("Dataset/statuses_unicode.txt", "r"):
        data.append(line[:-1])
    data = np.array(data)

    y_O = np.zeros(1)
    y_C = np.zeros(1)
    y_E = np.zeros(1)
    y_A = np.zeros(1)
    y_N = np.zeros(1)
    i=0
    for line in open("Dataset/big5labels.txt", "r"):
        big5_str = line[:-1].split(" ")
        if i==0:
            y_O[0] = float(big5_str[0])
            y_C[0] = float(big5_str[1])
            y_E[0] = float(big5_str[2])
            y_A[0] = float(big5_str[3])
            y_N[0] = float(big5_str[4])
        else:
            y_O = np.append(y_O, float(big5_str[0]))
            y_C = np.append(y_C, float(big5_str[1]))
            y_E = np.append(y_E, float(big5_str[2]))
            y_A = np.append(y_A, float(big5_str[3]))
            y_N = np.append(y_N, float(big5_str[4]))
        i += 1

    return [data, y_O, y_C, y_E, y_A, y_N]

def parseMyPersonality():
    #9913 lines
    #AUTHID,"STATUS","sEXT","sNEU","sAGR","sCON","sOPN","cEXT","cNEU","cAGR","cCON","cOPN",
    #"DATE","NETWORKSIZE","BETWEENNESS","NBETWEENNESS","DENSITY","BROKERAGE","NBROKERAGE","TRANSITIVITY"
    data = []
    y_O = []
    y_C = []
    y_E = []
    y_A = []
    y_N = []

    #parse the dataset file one line at a time
    for line in open("Dataset/mypersonality_final.csv", "r"):
        user_id = line.split(',')[0][1:]
        status = line.split(user_id)[1][3:].split('"",')[0]
        big5 = line.split(status)[1][3:].split(',""')[0].split(",")

        data.append(status)
        y_E.append(big5[0])
        y_N.append(big5[1])
        y_A.append(big5[2])
        y_C.append(big5[3])
        y_O.append(float(big5[4]))

    if not os.path.exists("Dataset"):
        os.makedirs("Dataset")

    fp = open("Dataset/statuses.txt", "w")
    for status in data:
        fp.write(status+"\n")
    fp.close()
    fp = open("Dataset/big5labels.txt", "w")
    for i in range(0,len(data)):
        fp.write(str(y_O[i])+" "+str(y_C[i])+" "+str(y_E[i])+" "+str(y_A[i])+" "+str(y_N[i])+"\n")
    fp.close()

    print("Files written.")
    return [np.array(data), np.array(y_O), np.array(y_C), np.array(y_E), np.array(y_A), np.array(y_N)]
