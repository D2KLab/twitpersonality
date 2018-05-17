from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import numpy as np
import datasetUtils as dsu
import embeddings
import sys
import os
import re

dataset_path = "../../FastText/dataset.vec"
tweet_threshold = 3

vectorizer = CountVectorizer(stop_words="english", analyzer="word")
analyzer = vectorizer.build_analyzer()

username = input("Enter username: ")
if username.startswith("@"):
    username = username.strip("@")

tweet_file_path = "Data/"+username+"/"+username+"_tweets.txt"

if not os.path.isfile(tweet_file_path):
    print("The user does not exist.")
    sys.exit(1)

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
print("Loading embeddings dataset...")
wordDictionary = dsu.parseFastText(dataset_path)
print("Data successfully loaded.")

try:
    tweetEmbeddings = embeddings.transformTextForTesting(wordDictionary, tweet_threshold, filteredTweets, "conc")
    print("Embeddings computed.\n")
except:
    #most of tweets are ingored for brevity/no embedding correspondence
    print("Not enough tweets for prediction.")
    sys.exit(1)

#load the saved ML models
for trait in ["O","C","E","A","N"]:
    model = joblib.load("Models/SVM_fasttext_conc_"+trait+".pkl")
    mean = np.mean(tweetEmbeddings, axis = 0)
    score = model.predict([mean])
    print("Score for",trait,"is:",str(score[0])[0:5])