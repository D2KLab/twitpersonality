from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.externals import joblib
from operator import add
import numpy as np
from timeit import default_timer as timer
import os
import fastTextParser
import trainModels

#read train data from parsed dataset files
print("Loading train data...")
data = []
for line in open("Dataset/statuses.txt", "r"):
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

print("Train data successfully loaded.")

#load word embeddings
wordDictionary = fastTextParser.parseData()

#istantiate CountVectorizer and get the analyzer handle
vectorizer = CountVectorizer(stop_words="english", analyzer="word")
analyzer = vectorizer.build_analyzer()
#create the vocabulary from the train data (size: 15185)
vectorizer.fit(data)

#take a subset of the train set that will be used for test
#need to implement 10-fold cross-validation
test_index = 10
test_data = data[0:(test_index-1)]
data = data[test_index:]

#pass each status to the analyzer and convert each of the resulting
#words in embeddings, them sum them up

#used to compute statistics
unique_words = []
tot_words = 0
skip_words = 0
skip_statuses = 0

#ignore posts with 0 tokens
length_threshold = 1
statuses_embeddings = []
i = 0
#process each post separately
for status in data:
    #preprocess post (preprocessor + tokenizer)
    words = analyzer(status)
    if len(words) < length_threshold:
        #need to remove corresponding entry from each of the big5 lists
        skip_statuses += 1
        y_O = np.delete(y_O, i)
        y_C = np.delete(y_C, i)
        y_E = np.delete(y_E, i)
        y_A = np.delete(y_A, i)
        y_N = np.delete(y_N, i)
        continue
    sum_embeddings = np.zeros(300, dtype=np.float)
    #get embedding of each word and sum them
    for word in words:
        tot_words += 1
        try:
            #get the embedding as string and transform it into vector of float of size 300
            word_embedding_string = wordDictionary[word]
            word_embedding = np.array(list(float(value) for value in word_embedding_string[:-1].split(" ")))
            sum_embeddings = sum_embeddings + word_embedding
        except KeyError:
            #no embedding exists for this word, ignore it
            skip_words += 1
            if word not in unique_words:
                unique_words.append(word)
            continue
    #skip posts with too many unrecognised words
    if len(post_embeddings) == 0:
        skip_statuses += 1
        y_O = np.delete(y_O, i)
        y_C = np.delete(y_C, i)
        y_E = np.delete(y_E, i)
        y_A = np.delete(y_A, i)
        y_N = np.delete(y_N, i)
        continue
    i += 1
    statuses_embeddings.append(sum_embeddings)

print("Length of posts embeddings: %d"%len(statuses_embeddings))
print("Total words: %d"%tot_words)
print("Ignored words: %d"%skip_words)
print("Unique words: %d"%len(unique_words))
print("Ignored posts: %d"%skip_statuses)

start = timer()
#train linear regression models
#to train SVM models, just call trainModels.SVM()
classifierO = trainModels.LReg(statuses_embeddings, y_O[test_index:])[0]
classifierC = trainModels.LReg(statuses_embeddings, y_C[test_index:])[0]
classifierE = trainModels.LReg(statuses_embeddings, y_E[test_index:])[0]
classifierA = trainModels.LReg(statuses_embeddings, y_A[test_index:])[0]
[classifierN, model] = trainModels.LReg(statuses_embeddings, y_N[test_index:])
end = timer()
print("Models trained in %.5f seconds"%(end-start))

#save models on disk
if not os.path.exists("LearnedModels"):
    os.makedirs("LearnedModels")
if model == "LReg":
    if not os.path.exists("LearnedModels/LinearRegression"):
        os.makedirs("LearnedModels/LinearRegression")
    joblib.dump(classifierO, "LearnedModels/LinearRegression/LinearReg_O.pkl")
    joblib.dump(classifierC, "LearnedModels/LinearRegression/LinearReg_C.pkl")
    joblib.dump(classifierE, "LearnedModels/LinearRegression/LinearReg_E.pkl")
    joblib.dump(classifierA, "LearnedModels/LinearRegression/LinearReg_A.pkl")
    joblib.dump(classifierN, "LearnedModels/LinearRegression/LinearReg_N.pkl")
elif model == "SVM":
    if not os.path.exists("LearnedModels/SVM"):
        os.makedirs("LearnedModels/SVM")
    joblib.dump(classifierO, "LearnedModels/SVM/SVM_O.pkl")
    joblib.dump(classifierC, "LearnedModels/SVM/SVM_C.pkl")
    joblib.dump(classifierE, "LearnedModels/SVM/SVM_E.pkl")
    joblib.dump(classifierA, "LearnedModels/SVM/SVM_A.pkl")
    joblib.dump(classifierN, "LearnedModels/SVM/SVM_N.pkl")

#test1: compute sum of embeddings and feed it to the model
test_embedding = np.zeros(300)
#same post processing as before
for string in test_data:
    words_tokens = analyzer(string)
    for word in words_tokens:
        try:
            word_embedding_string = wordDictionary[word]
            word_embedding = np.array(list(float(value) for value in word_embedding_string[:-1].split(" ")))
            test_embedding = test_embedding + word_embedding
        except KeyError:
            #ignore word
            continue
#predict scores for each trait
resultO = classifierO.predict([test_embedding])
resultC = classifierC.predict([test_embedding])
resultE = classifierE.predict([test_embedding])
resultA = classifierA.predict([test_embedding])
resultN = classifierN.predict([test_embedding])

print("test1\tO:\t",resultO)
print("test1\tC:\t",resultC)
print("test1\tE:\t",resultE)
print("test1\tA:\t",resultA)
print("test1\tN:\t",resultN, end="\n\n")

#test2: predict score for each word and average them
sumO = 0
sumC = 0
sumE = 0
sumA = 0
sumN = 0
used_words = 0
for string in test_data:
    words_tokens = analyzer(string)
    for word in words_tokens:
        try:
            word_embedding_string = wordDictionary[word]
            word_embedding = np.array(list(float(value) for value in word_embedding_string[:-1].split(" ")))

            score = classifierO.predict([word_embedding])
            sumO = sumO + score

            score = classifierC.predict([word_embedding])
            sumC = sumC + score

            score = classifierE.predict([word_embedding])
            sumE = sumE + score

            score = classifierA.predict([word_embedding])
            sumA = sumA + score

            score = classifierN.predict([word_embedding])
            sumN = sumN + score

            used_words += 1
        except KeyError:
            #ignore ?
            continue
resultO = sumO/used_words
resultC = sumC/used_words
resultE = sumE/used_words
resultA = sumA/used_words
resultN = sumN/used_words

print("test2\tO:\t",resultO)
print("test2\tC:\t",resultC)
print("test2\tE:\t",resultE)
print("test2\tA:\t",resultA)
print("test2\tN:\t",resultN)
