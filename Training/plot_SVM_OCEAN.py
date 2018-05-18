from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error
from scipy.stats.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.manifold import TSNE
import tsne
import datasetUtils as dsu
import embeddings
import sys
import os

#configs
method = "conc"
post_threshold = 3
x_scale = (0,5.5)
y_scale = (0,5.5)

def savePlot(y_true, y_pred, title, path):
    plt.clf()
    plt.xlim(x_scale)
    plt.ylim(y_scale)
    plt.plot(y_true, y_pred, '.')
    plt.ylabel('predicted values')
    plt.xlabel('actual values')
    plt.title(title)
    #plt.savefig(path)
    plt.show()

dataset = "fasttext"
#dataset = ""
dataset_path = "../FastText/dataset.vec"
#dataset_path = "D:\Downloads\datasetssss\Set9.bin"
shuffle = "yes"

posts = []
yO = []
yC = []
yE = []
yA = []
yN = []

print("[SVM] Loading myPersonality...")
[posts, yO, yC, yE, yA, yN] = dsu.readMyPersonality()
print("[SVM] Loading embeddings dataset...")
if dataset == 'fasttext':
    transform = True
    wordDictionary = dsu.parseFastText(dataset_path)
    #res = dsu.parseFastText(dataset_path)
    #wordDictionary = res[0]
    #wordWrods = res[1]
else:
    transform = False
    wordDictionary = dsu.loadEmbeddingsDataset(dataset_path, True)
print("[SVM] Data successfully loaded.")

if shuffle == 'True' or shuffle == 'yes' or shuffle == 'true':
    s = np.arange(posts.shape[0])
    np.random.shuffle(s)
    posts = posts[s]
    yO = yO[s]
    yC = yC[s]
    yE = yE[s]
    yA = yA[s]
    yN = yN[s]
    print("Data shuffled.")

#only for test
subsetSize = len(posts)
#ssubsetSize = 7500
subsetSize = 1000
posts = posts[0:subsetSize]
yO = yO[0:subsetSize]
yC = yC[0:subsetSize]
yE = yE[0:subsetSize]
yA = yA[0:subsetSize]
yN = yN[0:subsetSize]

old_yO = yO
old_yC = yC
old_yE = yE
old_yA = yA
old_yN = yN
[conE, yO, yC, yE, yA, yN] = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, method, transform)
print("Embeddings computed.")

split_index = round(len(conE)*0.85)
data_train = conE[:split_index]
data_test = conE[split_index:]

l = 1
for labels in [yO, yC, yE, yA, yN]:

    if l==1:
        big5trait = "O"
        print("[SVM] computing results for Openness...")
    elif l==2:
        big5trait = "C"
        print("[SVM] computing results for Conscientiousness...")
    elif l==3:
        big5trait = "E"
        print("[SVM] computing results for Extraversion...")
    elif l==4:
        big5trait = "A"
        print("[SVM] computing results for Agreeableness...")
    elif l==5:
        big5trait = "N"
        print("[SVM] computing results for Neuroticism...")
    l += 1

    model = SVR(kernel='rbf', gamma = 10, C=1).fit(data_train,labels[:split_index])
    res = model.predict(data_test)


    mse = mean_squared_error(labels[split_index:], res)
    title = big5trait + "_" + method + "_rbf_gamma10_C1\n"+str(round(mse,3))[0:5]
    savePlot(labels[split_index:], res, title, "Plots/"+method+"/"+title.split("\n")[0]+".png")