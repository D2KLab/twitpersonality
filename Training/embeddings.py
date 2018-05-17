from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

#the function expects documents to be a list of documents. To use just one document, pass [[document]]
def transformTextForTraining(embed_dictionary, length_threshold, documents, y_O, y_C, y_E, y_A, y_N, operation, FastText, friends=None):
    vectorizer = CountVectorizer(stop_words="english", analyzer="word")
    analyzer = vectorizer.build_analyzer()
    tokenizer = vectorizer.build_tokenizer()

    string = False
    deleted = 0

    if type(documents) is str: #single post
        string = True
        documents = [documents]

    text_embeddings = []
    i = 0

    for document in documents:
        words = analyzer(document)
        #words = tokenizer(document)
        if len(words) < length_threshold and not string:
            deleted += 1
            y_O = np.delete(y_O, i)
            y_C = np.delete(y_C, i)
            y_E = np.delete(y_E, i)
            y_A = np.delete(y_A, i)
            y_N = np.delete(y_N, i)
            if friends is not None:
                friends = np.delete(friends, i)
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
        if len(doc_embeddings) == 0 and not string:
            deleted += 1
            y_O = np.delete(y_O, i)
            y_C = np.delete(y_C, i)
            y_E = np.delete(y_E, i)
            y_A = np.delete(y_A, i)
            y_N = np.delete(y_N, i)
            if friends is not None:
                friends = np.delete(friends, i)
            continue

        if len(doc_embeddings) == 0:
            return False

        if friends is not None:
            if operation=="sum":
                text_embeddings.append(  np.append(np.sum(np.array(doc_embeddings),axis=0),friends[i])  )
            elif operation == "max":
                text_embeddings.append(np.append(np.amax(np.array(doc_embeddings),axis=0),friends[i]) )
            elif operation == "min":
                text_embeddings.append(np.append(np.amin(np.array(doc_embeddings),axis=0),friends[i]) )
            elif operation == "avg":
                text_embeddings.append(np.append(np.mean(np.array(doc_embeddings),axis=0),friends[i]) )
            elif operation == "conc":
                npmax = np.amax(np.array(doc_embeddings),axis=0)
                npmin = np.amin(np.array(doc_embeddings),axis=0)
                npavg = np.mean(np.array(doc_embeddings),axis=0)
                text_embeddings.append( np.append(np.concatenate((npmax, npmin, npavg)),friends[i]) )
        else:
            if operation=="sum":
                text_embeddings.append(np.sum(np.array(doc_embeddings),axis=0))
            elif operation == "max":
                text_embeddings.append(np.amax(np.array(doc_embeddings),axis=0))
            elif operation == "min":
                text_embeddings.append(np.amin(np.array(doc_embeddings),axis=0))
            elif operation == "avg":
                text_embeddings.append(np.mean(np.array(doc_embeddings),axis=0))
            elif operation == "conc":
                npmax = np.amax(np.array(doc_embeddings),axis=0)
                npmin = np.amin(np.array(doc_embeddings),axis=0)
                npavg = np.mean(np.array(doc_embeddings),axis=0)
                text_embeddings.append(np.concatenate((npmax, npmin, npavg)))
    i += 1

    if friends is not None:
        return [np.array(text_embeddings), y_O, y_C, y_E, y_A, y_N, friends]
    else:
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
        elif operation == "conc":
            npmax = np.amax(np.array(doc_embeddings),axis=0)
            npmin = np.amin(np.array(doc_embeddings),axis=0)
            npavg = np.mean(np.array(doc_embeddings),axis=0)
            text_embeddings.append(np.concatenate((npmax, npmin, npavg)))

    if len(text_embeddings) == 0:
        raise StandardError

    return np.array(text_embeddings)
