from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.externals import joblib
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

training_samples = []
yO = []
yC = []
yE = []
yA = []
yN = []

for line in open("users_embeddings3.csv","r"):
    parts = line[:-1].split(",")
    yO.append(float(parts[1]))
    yC.append(float(parts[2]))
    yE.append(float(parts[3]))
    yA.append(float(parts[4]))
    yN.append(float(parts[5]))
    embed = np.array(list(float(elem) for elem in parts[6:]),dtype=float)
    training_samples.append(embed)

training_samples = np.array(training_samples)
yO = np.array(yO)
yC = np.array(yC)
yE = np.array(yE)
yA = np.array(yA)
yN = np.array(yN)
print("Training set loaded. Total samples:",len(training_samples))

subsetSize = 30000
training_samples = training_samples[0:subsetSize]
yO = yO[0:subsetSize]
yC = yC[0:subsetSize]
yE = yE[0:subsetSize]
yA = yA[0:subsetSize]
yN = yN[0:subsetSize]

#shuffle data
s = np.arange(training_samples.shape[0])
np.random.shuffle(s)
training_samples = training_samples[s]
yO = yO[s]
yC = yC[s]
yE = yE[s]
yA = yA[s]
yN = yN[s]
print("Data shuffled.")

trait = 5
for labels in [yN]:

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

    model = SVR(kernel='rbf', gamma = gamma, C=C).fit(training_samples,labels)
    model_name = "SVM_Big_conc_"+big5trait+"_userWise.pkl"
    joblib.dump(model, "Models/MPBig/"+model_name)