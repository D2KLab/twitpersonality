from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os

#9913 lines
##AUTHID,"STATUS","sEXT","sNEU","sAGR","sCON","sOPN","cEXT","cNEU","cAGR","cCON","cOPN","DATE","NETWORKSIZE","BETWEENNESS","NBETWEENNESS","DENSITY","BROKERAGE","NBROKERAGE","TRANSITIVITY"

#parse dataset
data_perUser = []
data_all = []
y_O = []
y_C = []
y_E = []
y_A = []
y_N = []

#parse dataset file
old_id = ""
i=0
for line in open("mypersonality_final.csv", "r"):
    user_id = line.split(',')[0][1:]
    status = line.split(user_id)[1][3:].split('"",')[0]
    big5 = line.split(status)[1][3:].split(',""')[0].split(",")

    data_all.append(status)

    if old_id == "":
        old_id = user_id
        data_perUser.append([status])
        y_O.append(float(big5[4]))
        y_C.append(float(big5[3]))
        y_E.append(float(big5[0]))
        y_A.append(float(big5[2]))
        y_N.append(float(big5[1]))
    elif old_id != user_id:
        i=i+1
        old_id = user_id
        data_perUser.append([status])
        y_O.append(float(big5[4]))
        y_C.append(float(big5[3]))
        y_E.append(float(big5[0]))
        y_A.append(float(big5[2]))
        y_N.append(float(big5[1]))
    else:
        data_perUser[i].append(status)

num_users = len(data_perUser)
num_posts = len(data_all)
num_words = 0
num_chars = 0
for post in data_all:
    num_words += len(post.split(" "))
    num_chars += len(post)
avg_posts = num_posts/num_users
max_posts = max(len(user) for user in data_perUser)
min_posts = min(len(user) for user in data_perUser)
avg_len_words = int(sum(len(post.split(" ")) for post in data_all)/num_posts)
max_len_words = max(len(post.split(" ")) for post in data_all)
min_len_words = min(len(post.split(" ")) for post in data_all)
avg_len_chars = int(sum(len(post) for post in data_all)/num_posts)
max_len_chars = max(len(post) for post in data_all)
min_len_chars = min(len(post) for post in data_all)

vectorizer = CountVectorizer(stop_words="english", analyzer="word")
analyzer = vectorizer.build_analyzer()

avg_len_words_tok = int(sum(len(analyzer(post)) for post in data_all)/num_posts )
max_len_words_tok = max(len(analyzer(post)) for post in data_all)
min_len_words_tok = min(len(analyzer(post)) for post in data_all)
avg_len_chars_tok = int(sum(len(" ".join(analyzer(post))) for post in data_all)/num_posts)
max_len_chars_tok = max(len(" ".join(analyzer(post))) for post in data_all)
min_len_chars_tok = min(len(" ".join(analyzer(post))) for post in data_all)

avgO = float(sum(value for value in y_O )/len(y_O))
maxO = float(max(value for value in y_O))
minO = float(min(value for value in y_O))
avgC = float(sum(value for value in y_C)/len(y_C))
maxC = float(max(value for value in y_C))
minC = float(min(value for value in y_C))
avgE = float(sum(value for value in y_E)/len(y_E))
maxE = float(max(value for value in y_E))
minE = float(min(value for value in y_E))
avgA = float(sum(value for value in y_A)/len(y_A))
maxA = float(max(value for value in y_A))
minA = float(min(value for value in y_A))
avgN = float(sum(value for value in y_N)/len(y_N))
maxN = float(max(value for value in y_N))
minN = float(min(value for value in y_N))

stdO = np.std(np.array(y_O))
stdC = np.std(np.array(y_C))
stdE = np.std(np.array(y_E))
stdA = np.std(np.array(y_A))
stdN = np.std(np.array(y_N))

#write statistics in a file
fp = open("Dataset/statistics.txt", "w")
fp.write("--------------------- General statistics ----------------\n")
fp.write("\tNumber of users\t%d\n" %num_users)
fp.write("\tNumber of posts\t%d\n" %num_posts)
fp.write("\tTotal words\t%d\n" %num_words)
fp.write("\tTotal characters\t%d\n" %num_chars)
fp.write("\n---------------- Posts statistics ----------------\n")
fp.write("\tAverage posts per user\t%d\n" %avg_posts)
fp.write("\tHighest number of posts per user\t%d\n" %max_posts)
fp.write("\tLowest number of posts\t%d\n" %min_posts)
fp.write("\n---------------- Words per post statistics ----------------\n")
fp.write("\tAverage words\t%d\n" %avg_len_words)
fp.write("\tHighest number of words\t%d\n" %max_len_words)
fp.write("\tLowest number of words\t%d\n" %min_len_words)
fp.write("\tAverage words after preprocessing\t%d\n" %avg_len_words_tok)
fp.write("\tHighest number of words after preprocessing\t%d\n" %max_len_words_tok)
fp.write("\tLowest number of words after preprocessing\t%d\n" %min_len_words_tok)
fp.write("\n---------------- Characters per post statistics ----------------\n")
fp.write("\tAverage characters\t%d\n" %avg_len_chars)
fp.write("\tHighest number of characters\t%d\n" %max_len_chars)
fp.write("\tLowest number of characters\t%d\n" %min_len_chars)
fp.write("\tAverage characters after preprocessing\t%d\n" %avg_len_chars_tok)
fp.write("\tHighest number of characters after preprocessing\t%d\n" %max_len_chars_tok)
fp.write("\tLowest number of characters after preprocessing\t%d\n" %min_len_chars_tok)
fp.write("\n---------------- Big5 traits statistics ----------------\n")
fp.write("\tAverage\tOPE\t%.2f\n"%avgO)
fp.write("\tHighest\tOPE\t%.2f\n"%maxO)
fp.write("\tLowest\tOPE\t%.2f\n"%minO)
fp.write("\tStd\t\tOPE\t%.3f\n\n"%stdO)
fp.write("\tAverage\tCON\t%.2f\n"%avgC)
fp.write("\tHighest\tCON\t%.2f\n"%maxC)
fp.write("\tLowest\tCON\t%.2f\n"%minC)
fp.write("\tStd\t\tCON\t%.3f\n\n"%stdC)
fp.write("\tAverage\tEXT\t%.2f\n"%avgE)
fp.write("\tHighest\tEXT\t%.2f\n"%maxE)
fp.write("\tLowest\tEXT\t%.2f\n"%minE)
fp.write("\tStd\t\tEXT\t%.3f\n\n"%stdE)
fp.write("\tAverage\tAGR\t%.2f\n"%avgA)
fp.write("\tHighest\tAGR\t%.2f\n"%maxA)
fp.write("\tLowest\tAGR\t%.2f\n"%minA)
fp.write("\tStd\t\tAGR\t%.3f\n\n"%stdA)
fp.write("\tAverage\tNEU\t%.2f\n"%avgN)
fp.write("\tHighest\tNEU\t%.2f\n"%maxN)
fp.write("\tLowest\tNEU\t%.2f\n"%minN)
fp.write("\tStd\t\tNEU\t%.3f\n\n"%stdN)
fp.close()
