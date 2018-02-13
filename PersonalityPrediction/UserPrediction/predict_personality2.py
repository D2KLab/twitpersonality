from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
from pathlib import Path
import numpy as np
import datasetUtils as dsu
import embeddings
import sys
import os
import re

dataset_path = "../FastText/dataset.vec"
tweet_threshold = 3

vectorizer = CountVectorizer(stop_words="english", analyzer="word")
analyzer = vectorizer.build_analyzer()

usernames = []
search_input = input("enter username or filename:")
if not Path(search_input).is_file():
	#entered username
    if search_input.startswith("@"):
        search_input = search_input.strip("@")
    usernames.append(search_input)
else:
	#entered file name
    if os.stat(Path(search_input)).st_size == 0:
        sys.exit("Error. File is empty.")
    for name in open(search_input, "r"):        
        if name[-1] == "\n":
            name = name[:-1]
        usernames.append(name)

print("Loading embeddings dataset...")
wordDictionary = dsu.parseFastText(dataset_path)
print("Data successfully loaded.")

outfile = []
for username in usernames:
    tweet_file_path = "Data/"+username+"/"+username+"_tweets.txt"

    if not os.path.isfile(tweet_file_path):
        print("Error. Cannot find tweets for username",username)
        continue

    filteredTweets = []
    #preprocess tweets
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

        if len(filteredTweets) == 0:
            print("Not enough tweets for prediction.")
            sys.exit(1)

    #now we can process the tweet using embeddings.transofrmTextForTraining
    try:
        tweetEmbeddings = embeddings.transformTextForTesting(wordDictionary, tweet_threshold, filteredTweets, "conc")
        print("Embeddings computed.")
    except:
        #most of tweets are ingored for brevity/no embedding correspondence
        print("Not enough tweets for prediction.")
        continue

    scores = {}
    #load the saved ML models
    for trait in ["O","C","E","A","N"]:
        model = joblib.load("Models/SVM_fasttext_conc_"+trait+".pkl")
        mean = np.mean(tweetEmbeddings, axis = 0)
        score = model.predict([mean])
        scores[trait] = float(str(score[0])[0:5])
        print("\nScore for",trait,"is:",str(score[0])[0:5])

    jung = ""
    if scores["E"] > 3:
        jung = "E"
    else:
        jung = "I"
    if scores["O"] > 3:
        jung = jung + "N"
    else:
        jung = jung + "S"
    if scores["A"] > 3:
        jung = jung + "F"
    else:
        jung = jung + "T"
    if scores["C"] > 3:
        jung = jung + "J"
    else:
        jung = jung + "P"

    print("Jungian type is",jung)

    outfile.append(username+","+str(scores["O"])+","+str(scores["C"])+","+str(scores["E"])+","+str(scores["A"])+","+str(scores["N"])+","+jung)

filename = "personality_predictions2.csv"
fp = open(filename,"w")
for elem in outfile:
    fp.write(elem+"\n")
fp.close()