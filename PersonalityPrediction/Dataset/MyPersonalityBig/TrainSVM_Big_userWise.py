from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.svm import SVR
from pathlib import Path
import pandas as pd
import numpy as np
import datasetUtils as dsu
import embeddings
import sys
import os

#configs
post_threshold = 3
dataset_path = "../FastText/dataset.vec"
posts_path = "join.csv"

users_subsets = list(int(num) for num in sys.argv[1:])

if os.path.exists("MPBig_results_userWise.csv"):
    os.remove("MPBig_results_userWise.csv")

types = {"userid":str,"ope":float,"con":float,"ext":float,"agr":float,"neu":float,"message":str}
print("Loading training set...")
df = pd.read_csv(posts_path, usecols=[0,1,2,3,4,5,6], dtype=types, error_bad_lines=False, engine="python")
print("Training set correctly loaded.")

print("Loading embeddings dataset...")
wordDictionary = dsu.parseFastText(dataset_path)
print("Dataset correctly loaded.")

#get unique userids
userids = df["userid"].unique()
#shuffle data
s = np.arange(userids.shape[0])
np.random.shuffle(s)
userids = userids[s]

for subset in users_subsets:
    print("Number of users:",subset)
    ids = userids[0:subset]

    training_samples = []
    yO = []
    yC = []
    yE = []
    yA = []
    yN = []

    for uid in ids:
        userdf = df[df["userid"]==uid]
        messages = np.array(userdf["message"],dtype=pd.Series)
        ope = userdf["ope"].iloc[0]
        con = userdf["con"].iloc[0]
        ext = userdf["ext"].iloc[0]
        agr = userdf["agr"].iloc[0]
        neu = userdf["neu"].iloc[0]
        yO.append(userdf["ope"].iloc[0])
        yC.append(userdf["con"].iloc[0])
        yE.append(userdf["ext"].iloc[0])
        yA.append(userdf["agr"].iloc[0])
        yN.append(userdf["neu"].iloc[0])
        training_samples.append({"userid":uid,"messages":messages,"O":ope,"C":con,"E":ext,"A":agr,"N":neu})

    for sample in training_samples:
        size = len(sample["messages"])
        conE = embeddings.transformTextForTraining(wordDictionary, post_threshold, sample["messages"], np.full(size,sample["O"],dtype=float), np.full(size,sample["C"],dtype=float), np.full(size,sample["E"],dtype=float), np.full(size,sample["A"],dtype=float), np.full(size,sample["N"],dtype=float), "conc", True)[0]
        sample["messages"] = conE
    print("Word embeddings computed.")

    training_samples = np.array(training_samples)
    yO = np.array(yO)
    yC = np.array(yC)
    yE = np.array(yE)
    yA = np.array(yA)
    yN = np.array(yN)

    s = np.arange(training_samples.shape[0])
    np.random.shuffle(s)
    training_samples = training_samples[s]
    yO = yO[s]
    yC = yC[s]
    yE = yE[s]
    yA = yA[s]
    yN = yN[s]

    mse_OCEAN = {"O":[],"C":[],"E":[],"A":[],"N":[]}

    k_fold = KFold(n_splits=4)
    it = 1
    for train, test in k_fold.split(training_samples):
        
        posts = []
        yO_train = []
        yC_train = []
        yE_train = []
        yA_train = []
        yN_train = []

        print("CV iteration",it)
        for sample in np.array(training_samples)[train]:
            for message in sample["messages"]:
                posts.append(message)
                yO_train.append(sample["O"])
                yC_train.append(sample["C"])
                yE_train.append(sample["E"])
                yA_train.append(sample["A"])
                yN_train.append(sample["N"])

        trait = 1
        for labels in [yO_train, yC_train, yE_train, yA_train, yN_train]:

            if trait==1:
                big5trait = "O"
                gamma = 1
                C = 1
                print("   Training model for Openness...")
            elif trait==2:
                big5trait = "C"
                gamma = 1
                C = 1
                print("   Training model for Conscientiousness...")
            elif trait==3:
                big5trait = "E"
                gamma = 1
                C = 10
                print("   Training model for Extraversion...")
            elif trait==4:
                big5trait = "A"
                gamma = 1
                C = 1
                print("   Training model for Agreeableness...")
            elif trait==5:
                big5trait = "N"
                gamma = 10
                C = 10
                print("   Training model for Neuroticism...")
            trait += 1

            model = SVR(kernel='rbf', gamma = gamma, C=C).fit(posts,labels)

            mses = []
            for sample in np.array(training_samples)[test]:
                if len(sample["messages"]) == 0:
                    continue
                if len(sample["messages"]) == 900:
                    preds = model.predict(sample["messages"].reshape(1, -1))
                else:
                    preds = model.predict(sample["messages"])
                mse = mean_squared_error( preds, np.full(len(sample["messages"]),sample[big5trait],dtype=float))
                mses.append(mse)
            mse_OCEAN[big5trait].append(np.mean(np.array(mses)))

        it += 1
        
    for trait in ["O","C","E","A","N"]:
        trait_mse = np.mean(np.array(mse_OCEAN[trait]))
        print("\tAverage MSE for",trait,":",trait_mse)
        with open("MPBig_results_userWise.csv", "a") as outfile:
            outfile.write(trait+","+str(subset)+","+str(len(posts))+","+str(trait_mse)+"\n")
