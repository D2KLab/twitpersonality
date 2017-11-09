from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

#the function expects documents to be a list of documents. To use just one document, pass [[document]]
def transformTextForTraining(embed_dictionary, length_threshold, documents, y_O, y_C, y_E, y_A, y_N, operation, FastText):
    vectorizer = CountVectorizer(stop_words="english", analyzer="word")
    analyzer = vectorizer.build_analyzer()

    text_embeddings = []
    i = 0
    for document in documents:
        words = analyzer(document)
        if len(words) < length_threshold:
            y_O = np.delete(y_O, i)
            y_C = np.delete(y_C, i)
            y_E = np.delete(y_E, i)
            y_A = np.delete(y_A, i)
            y_N = np.delete(y_N, i)
            continue
        doc_embeddings = []
        for word in words:
            try:
                word_embedding = embed_dictionary[word]
                if FastText:
                    word_embedding = np.array(list(float(value) for value in word_embedding[:-1].split(" ")))
                doc_embeddings.append(word_embedding)
            except KeyError:
                continue
        if len(doc_embeddings) == 0:
            y_O = np.delete(y_O, i)
            y_C = np.delete(y_C, i)
            y_E = np.delete(y_E, i)
            y_A = np.delete(y_A, i)
            y_N = np.delete(y_N, i)
            continue
        i += 1

        if operation=="sum":
            text_embeddings.append(np.sum(np.array(doc_embeddings),axis=0))
        elif operation == "max":
            text_embeddings.append(np.amax(np.array(doc_embeddings),axis=0))
        elif operation == "min":
            text_embeddings.append(np.amin(np.array(doc_embeddings),axis=0))
        elif operation == "avg":
            text_embeddings.append(np.mean(np.array(doc_embeddings),axis=0))
        elif operation == "con":
            npmax = np.amax(np.array(doc_embeddings),axis=0)
            npmin = np.amin(np.array(doc_embeddings),axis=0)
            npavg = np.mean(np.array(doc_embeddings),axis=0)
            text_embeddings.append(np.concatenate((npmax, npmin, npavg)))

    return [np.array(text_embeddings), y_O, y_C, y_E, y_A, y_N]

def transformTextForTesting(embed_dictionary, length_threshold, documents, operation):
    vectorizer = CountVectorizer(stop_words="english", analyzer="word")
    analyzer = vectorizer.build_analyzer()

    text_embeddings = []
    i = 0
    for document in documents:
        words = analyzer(document)
        if len(words) < length_threshold:
            #move to the next document
            continue
        doc_embeddings = []
        for word in words:
            try:
                word_embedding_string = embed_dictionary[word]
                word_embedding = np.array(list(float(value) for value in word_embedding_string[:-1].split(" ")))
                doc_embeddings.append(word_embedding)
            except KeyError:
                continue
        if len(doc_embeddings) == 0:
            continue
        i += 1

        if operation=="sum":
            text_embeddings.append(np.sum(np.array(doc_embeddings),axis=0))
        elif operation == "max":
            text_embeddings.append(np.amax(np.array(doc_embeddings),axis=0))
        elif operation == "min":
            text_embeddings.append(np.amin(np.array(doc_embeddings),axis=0))
        elif operation == "avg":
            text_embeddings.append(np.mean(np.array(doc_embeddings),axis=0))

    return np.array(text_embeddings)
