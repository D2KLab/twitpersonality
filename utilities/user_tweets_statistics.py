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
usersData = []
for username in usernames:
    print("Username:",username)
    tweet_file_path = "Data/"+username+"/"+username+"_tweets.txt"

    if not os.path.isfile(tweet_file_path):
        print("Error. Cannot find tweets for username",username)
        continue

    num_tweets = 0
    avg_words = []
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
            

        words = analyzer(tweet)
        if len(words) < tweet_threshold:
            continue
        else:
            num_tweets += 1

        num_words = 0
        for word in words:
            try:
                word_embedding = wordDictionary[word]
                num_words += 1
            except KeyError:
                continue
        avg_words.append(num_words)
    if num_tweets == 0:
            print("Not enough tweets for prediction.")
            continue
    usersData.append(username+","+str(num_tweets)+","+str(np.mean(np.array(avg_words))))
fp = open("TwitterUsersStats.csv", "w")
for elem in usersData:
    fp.write(elem+"\n")
fp.close()