from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.keyedvectors import KeyedVectors
import datasetUtils as dsu
import numpy as np

def countWords(embeddings_dataset):
    tot_words = 0
    found_words = 0
    for document in data:
        words = analyzer(document)
        if len(words) < 1:
            #move to the next document
            continue
        for word in words:
            tot_words += 1
            try:
                word_embedding = embeddings_dataset[word]
                found_words += 1
            except KeyError:
                continue
    return [tot_words, found_words]

print("Loading train data...")
[data, y_O, y_C, y_E, y_A, y_N] = dsu.readMyPersonality()

vectorizer = CountVectorizer(stop_words="english", analyzer="word")
analyzer = vectorizer.build_analyzer()

print("Loading Datasets...")
wordDictionary = dsu.parseFastText("../FastText/dataset.vec")
print("FastText loaded.")


#fp = open("Dataset/wordCoverage.txt", "w")

[words, hits] = countWords(wordDictionary)

print("tot_words:", words)
print("found_words:", hits)
print("word coverage: %.2f%%" %float((100*hits)/words))
"""
fp.write("Fastext\t\t"+str(words)+"\t"+str(hits)+"\t%.2f%%"%float((100*hits)/words))

for i in range(1,11):
    wordDictionary = KeyedVectors.load_word2vec_format('D:\Downloads\datasetssss\Set'+str(i)+'.bin', binary=True)
    print("Dataset",i,"loaded")

    [words, hits] = countWords(wordDictionary)
    print("tot_words:", words)
    print("found_words:", hits)
    print("word coverage: %.2f%%" %float((100*hits)/words))

    fp.write("Dataset "+str(i)+"\t\t"+str(words)+"\t"+str(hits)+"\t%.2f%%"%float((100*hits)/words))

fp.close()
"""
