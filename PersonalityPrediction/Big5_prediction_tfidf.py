from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LinearRegression

#read data from parsed dataset files
data = []
for line in open("Dataset/statuses.txt", "r"):
    data.append(line[:-1])
y_O = []
y_C = []
y_E = []
y_A = []
y_N = []
for line in open("Dataset/big5labels.txt", "r"):
    big5_str = line[:-1].split(" ")
    y_O.append(float(big5_str[0]))
    y_C.append(float(big5_str[1]))
    y_E.append(float(big5_str[2]))
    y_A.append(float(big5_str[3]))
    y_N.append(float(big5_str[4]))

print("Data successfully loaded.")

#to be deleted since we will use one different model for each big5 trait
big5_vector = list(map(lambda a, b, c, d, e: [a, b, c, d, e], y_O,y_C,y_E,y_A,y_N))

vectorizer = CountVectorizer(stop_words="english")
#build a matrix of word occurrencies (words are expressed as integers)
#word-integer mapping are stored into vectorizer.vocabulary_
res = vectorizer.fit_transform(data)
print("Word ids matrix dimension: %d %d" %res.shape)


tfidf_transformer = TfidfTransformer(norm="l2")
#build the tf-idf matrix from the word occurrencies matrix
tfidf_matrix = tfidf_transformer.fit_transform(res)
print("Tf-idf matrix dimension: %d %d" %tfidf_matrix.shape)

#text to be classified
input_text = ["Today is sunny and I will go for a walk in the park"]

#transform text into integers and compute words occurrencies
tf_matrix_test = vectorizer.transform(input_text)
#compute tf-idf using tf matrix
tfidf_matrix_test = tfidf_transformer.transform(tf_matrix_test)
print("Tf-idf test matrix dimension: %d %d" %tfidf_matrix_test.shape)

#train the model using mypersonality dataset
classifier = LinearRegression().fit(tfidf_matrix, big5_vector)
#use tf-idf matrix computed from input_text to predict personality
predict = classifier.predict(tfidf_matrix_test)
print("prediction:", predict[0])
