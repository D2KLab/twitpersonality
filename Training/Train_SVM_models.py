from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.externals import joblib
import numpy as np
from sklearn.svm import SVR
import datasetUtils as dsu
import embeddings
import os

#configs
method = "conc"
post_threshold = 3
dataset = "fasttext"
dataset_path = "../FastText/dataset.vec"

posts = []
yO = []
yC = []
yE = []
yA = []
yN = []

print("Loading myPersonality...")
[posts, yO, yC, yE, yA, yN] = dsu.readMyPersonality()
print("Loading embeddings dataset...")
wordDictionary = dsu.parseFastText(dataset_path)
print("Data successfully loaded.")

#shuffle data
s = np.arange(posts.shape[0])
np.random.shuffle(s)
posts = posts[s]
yO = yO[s]
yC = yC[s]
yE = yE[s]
yA = yA[s]
yN = yN[s]
print("Data shuffled.")

[conE, yO, yC, yE, yA, yN] = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, yO, yC, yE, yA, yN, method, True)
print("Embeddings computed.")

"""split_index = round(len(conE)*0.85)
data_train = conE[:split_index]
data_test = conE[split_index:]"""

l = 1
k_fold = KFold(n_splits=10)
for labels in [yO, yC, yE, yA, yN]:

    if l==1:
        big5trait = "O"
        gamma = 1
        C = 1
        print("Training model for Openness...")
    elif l==2:
        big5trait = "C"
        gamma = 1
        C = 1
        print("Training model for Conscientiousness...")
    elif l==3:
        big5trait = "E"
        gamma = 1
        C = 10
        print("Training model for Extraversion...")
    elif l==4:
        big5trait = "A"
        gamma = 1
        C = 1
        print("Training model for Agreeableness...")
    elif l==5:
        big5trait = "N"
        gamma = 10
        C = 10
        print("Training model for Neuroticism...")
    l += 1

    mses = []

    for train, test in k_fold.split(conE):
        model = SVR(kernel='rbf', gamma = gamma, C=C).fit(conE[train],labels[train])
        res = model.predict(conE[test])
        mse = mean_squared_error(res, labels[test])
        mses.append(mse)
    print("MSE",big5trait,":",np.mean(np.array(mses)))

