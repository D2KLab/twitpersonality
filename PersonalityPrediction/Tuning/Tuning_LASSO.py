from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error
from scipy.stats.stats import pearsonr
import numpy as np
from sklearn.linear_model import Lasso
import datasetUtils as dsu
import embeddings
import statistics
import sys
import os

#configs
post_threshold = 3
alpha_lasso = [1e-15, 1e-10, 1e-8, 1e-5, 1e-4, 1e-3, 1e-2, 1, 5, 10]

#parse cmd arguments
if len(sys.argv) != 5 or sys.argv[1] not in ['O','C','E','A','N','o','c','e','a','n'] or sys.argv[2] not in ['fasttext', 'dataset9'] or not os.path.exists(sys.argv[3]) or sys.argv[4] not in ['True', 'False', 'yes', 'no']:
    print("Usage:", sys.argv[0], "<BIG5_trait> <embeddings_dataset> <dataset_path> <shuffle_data>")
    print("\tBIG5_trait: [O, C, E, A, N, o, c, e, a, n]")
    print("\tembeddings_dataset: [fasttext, dataset9]")
    print("\tdataset_path: [path/to/the/file]")
    print("\tshuffle_data: [yes, no], [True, False]")
    sys.exit(1)
else:
    big5 = sys.argv[1].upper()
    dataset = sys.argv[2]
    dataset_path = sys.argv[3]
    shuffle = sys.argv[4]

posts = []
yO = []
yC = []
yE = []
yA = []
yN = []

print("Loading myPersonality...")
[posts, yO, yC, yE, yA, yN] = dsu.readMyPersonality()
print("Loading embeddings dataset...")
if dataset == 'fasttext':
    transform = True
    wordDictionary = dsu.parseFastText(dataset_path)
else:
    transform = False
    wordDictionary = dsu.loadEmbeddingsDataset(dataset_path)
print("Data successfully loaded.")

filename = "tuning_LASSO_"+big5+"_"+dataset

if shuffle == 'True' or shuffle == 'yes' or shuffle == 'true':
    s = np.arange(posts.shape[0])
    np.random.shuffle(s)
    posts = posts[s]
    yO = yO[s]
    yC = yC[s]
    yE = yE[s]
    yA = yA[s]
    yN = yN[s]
    filename = filename + "_shuffle"
    print("Data shuffled.")
else:
    filename = filename + "_noShuffle"

pcc_filename = filename + "_pcc.txt"
filename = filename + ".csv"

#save lists because transformTextForTraining() changes them
old_yO = yO
old_yC = yC
old_yE = yE
old_yA = yA
old_yN = yN

[sumE, yO, yC, yE, yA, yN]  = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "sum", transform)
maxE = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "max", transform)[0]
minE = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "min", transform)[0]
avgE = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "avg", transform)[0]
conE = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "con", transform)[0]

print("Word embeddings computed.")

if big5 == 'O':
    labels = yO
elif big5 == 'C':
    labels = yC
elif big5 == 'E':
    labels = yE
elif big5 == 'A':
    labels = yA
elif big5 == 'N':
    labels = yN

if not os.path.exists("Results"):
    os.makedirs("Results")
try:
    os.remove("Results/"+filename)
except FileNotFoundError:
    pass
try:
    os.remove("Results/"+pcc_filename)
except FileNotFoundError:
    pass

j = 1
k_fold = KFold(n_splits=10)
for data in [sumE, maxE, minE, avgE, conE]:

    if j==1:
        method = "sum"
        print("computing results for sum...")
    elif j==2:
        method = "max"
        print("computing results for max...")
    elif j==3:
        method = "min"
        print("computing results for min...")
    elif j==4:
        method = "avg"
        print("computing results for avg...")
    elif j==5:
        method = "conc"
        print("computing results for concat...")
    j += 1

    #3 error measures
    #10 alpha values - arr[0-9]
    #10 CV iterations - arr[0-9][0-9]
    scores_mse = np.zeros([10,10], dtype=np.float)
    scores_r2 = np.zeros([10,10], dtype=np.float)
    scores_pcc = np.zeros([10,10,2], dtype=np.float) #pcc also has p-value

    i=0
    for train, test in k_fold.split(data):
        print("[CV iteration %d]"%(i+1))
        z = 0
        for alpha in alpha_lasso:
            lassoreg = Lasso(alpha = alpha, normalize=True, max_iter = 1e5).fit(data[train], labels[train])
            res = lassoreg.predict(data[test])
            r2 = lassoreg.score(data[test], labels[test])
            mse = mean_squared_error(labels[test], res)
            pcc = pearsonr (labels[test], res)

            scores_mse[z][i] = mse
            scores_r2[z][i] = r2
            scores_pcc[z][i] = pcc

            z += 1
        i += 1

    fp = open("Results/"+filename, "a+")
    for value in range(0,len(scores_mse)):
        fp.write(method+",mse,alpha"+str(value+1)+","+str(np.mean(scores_mse[value]))+","+"\n")
    for value in range(0,len(scores_r2)):
        fp.write(method+",r2,alpha"+str(value+1)+","+str(np.mean(scores_r2[value]))+","+"\n")
    for value in range(0,len(scores_pcc)):
        pcc_only = np.array(list(scor[0] for scor in scores_pcc[value])) #extract only pcc score
        pcc_only = pcc_only[np.where(~np.isnan(pcc_only))] #filter out nan values

        if len(pcc_only) != 0:
            mean_score = np.mean(pcc_only)
        else: #all elements are nan
            mean_score = "nan"

        fp.write(method+",pcc,alpha"+str(value+1)+","+str(mean_score)+","+"\n")
    fp.close()

    fp = open("Results/"+pcc_filename, "a+")
    for value in range(0,len(scores_pcc)):
        fp.write(method+",pcc,alpha"+str(value+1)+"\n")
        for elem in scores_pcc[value]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
    fp.write("\n\n")
    fp.close()
