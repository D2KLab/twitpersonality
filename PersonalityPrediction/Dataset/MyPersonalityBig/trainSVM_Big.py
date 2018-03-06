from sklearn.metrics import mean_squared_error
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.svm import SVR
import datasetUtils as dsu
import embeddings
import os

#configs
post_threshold = 3
dataset_path = "../FastText/dataset.vec"


types = {"userid":str,"ope":float,"con":float,"ext":float,"agr":float,"neu":float,"message":str}
print("Loading training set...")
df = pd.read_csv("join.csv", usecols=[0,1,2,3,4,5,6], dtype=types, error_bad_lines=False, engine="python", nrows=5000000)
print("Training set correctly loaded.")

#shuffle
#TODO sostituire df.count()[0] con la massima dimensione del dataset che usiamo per il training (es. 100k)
dfs = df.sample(df.count()[0])
print("Training set shuffled.")

print("Loading embeddings dataset...")
wordDictionary = dsu.parseFastText(dataset_path)
print("Dataset correctly laoded.")

if os.path.exists("MPBig_results.csv"):
    os.remove("MPBig_results.csv")

training_sizes = [500,1000,2000,5000,10000,15000,20000,50000]

post_embeddings = []

for iterator in range(0,len(training_sizes)):
    size = training_sizes[iterator]
    print("Training models with size:",size)

    posts = dfs["message"].iloc[0:size]
    yO = np.array(dfs["ope"].iloc[0:size],dtype=pd.Series)
    yC = np.array(dfs["con"].iloc[0:size],dtype=pd.Series)
    yE = np.array(dfs["ext"].iloc[0:size],dtype=pd.Series)
    yA = np.array(dfs["agr"].iloc[0:size],dtype=pd.Series)
    yN = np.array(dfs["neu"].iloc[0:size],dtype=pd.Series)
    [conE, yO, yC, yE, yA, yN] = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, yO, yC, yE, yA, yN, "conc", True)
    print("\tEmbeddings computed.")

    trait = 1
    k_fold = KFold(n_splits=5)
    for labels in [yO, yC, yE, yA, yN]:

        if trait==1:
            big5trait = "O"
            gamma = 1
            C = 1
            print("\tTraining model for Openness...")
        elif trait==2:
            big5trait = "C"
            gamma = 1
            C = 1
            print("\tTraining model for Conscientiousness...")
        elif trait==3:
            big5trait = "E"
            gamma = 1
            C = 10
            print("\tTraining model for Extraversion...")
        elif trait==4:
            big5trait = "A"
            gamma = 1
            C = 1
            print("\tTraining model for Agreeableness...")
        elif trait==5:
            big5trait = "N"
            gamma = 10
            C = 10
            print("\tTraining model for Neuroticism...")
        trait += 1

        mses = []

        it = 1
        for train, test in k_fold.split(conE):
            print("\t\tcv iteration",it)
            model = SVR(kernel='rbf', gamma = gamma, C=C).fit(conE[train],labels[train])
            res = model.predict(conE[test])
            mse = mean_squared_error(res, labels[test])
            mses.append(mse)
            it+=1

        with open("MPBig_results.csv", "a") as outfile:
            outfile.write(big5trait+","+str(size)+","+str(np.mean(np.array(mses)))+"\n")