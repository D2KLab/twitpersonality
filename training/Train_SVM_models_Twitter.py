from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import numpy as np
import datasetUtils as dsu
import embeddings
import sys
import os
import re

dataset_path = "../FastText/dataset.vec"
tweet_threshold = 3
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
    plt.savefig(path)

print("Loading embeddings dataset...")
wordDictionary = dsu.parseFastText(dataset_path)
print("Data successfully loaded.")

filteredTweets = []
yO = []
yC = []
yE = []
yA = []
yN = []

for line in open("Data/questionnaires.csv", "r"):
    parts= line.split(";")

    username = parts[2]
    if username[0] == '@':
        username = username[1:]

    tweet_file_path = "Data/"+username+"/"+username+"_tweets.txt"

    for tweet in open(tweet_file_path, "r", encoding="utf-8"):

        if re.match(r'^(RT)', tweet):
            #ingore pure retweets (= with no associated text)
            continue
        #remove links starting with "http"
        tweet = re.sub(r'((http)([^\s]*)(\s|$))|((http)([^\s]*)$)', "", tweet)
        #remove links with no http (probably unnecessary)
        tweet = re.sub(r'(\s([^\s]*)\.([^\s]*)\/([^\s]*)\s)|(^([^\s]*)\.([^\s]*)\/([^\s]*)(\s|$))|(\s([^\s]*)\.([^\s]*)\/([^\s]*)$)', " ", tweet)
        #remove mentions
        tweet = re.sub(r'(\s(@)([^\s]*)\s)|((^@)([^\s]*)(\s|$))|(@([^\s]*)$)', " ", tweet)
        #hashtags are removed by countvectorizer

        filteredTweets.append(tweet)
        yO.append(float(parts[-10].replace(",",".")))
        yC.append(float(parts[-9].replace(",",".")))
        yE.append(float(parts[-8].replace(",",".")))
        yA.append(float(parts[-7].replace(",",".")))
        yN.append(float(parts[-6].replace(",",".")))

filteredTweets = np.array(filteredTweets)
yO = np.array(yO)
yC = np.array(yC)
yE = np.array(yE)
yA = np.array(yA)
yN = np.array(yN)

s = np.arange(filteredTweets.shape[0])
np.random.shuffle(s)
filteredTweets = filteredTweets[s]
yO = yO[s]
yC = yC[s]
yE = yE[s]
yA = yA[s]
yN = yN[s]
print("Data shuffled.")

[conE, yO, yC, yE, yA, yN] = embeddings.transformTextForTraining(wordDictionary, tweet_threshold, filteredTweets, yO, yC, yE, yA, yN, "conc", True)
print("Embeddings computed.")

l = 1
k_fold = KFold(n_splits=4)
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
        title = big5trait + "_Twitter" + "\n" + str(round(mse,4))[0:6]
        savePlot(labels[test], res, title, "Data/PLOTS/Twitter_models/"+title.split("\n")[0]+".png")

    print("MSE",big5trait,":",np.mean(np.array(mses)))

