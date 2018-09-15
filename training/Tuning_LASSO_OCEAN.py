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
if len(sys.argv) != 4 or sys.argv[1] not in ['fasttext', 'dataset9'] or not os.path.exists(sys.argv[2]) or sys.argv[3] not in ['True', 'False', 'yes', 'no']:
    print("Usage:", sys.argv[0], "<embeddings_dataset> <dataset_path> <shuffle_data>")
    print("\tembeddings_dataset: [fasttext, dataset9]")
    print("\tdataset_path: [path/to/the/file]")
    print("\tshuffle_data: [yes, no], [True, False]")
    sys.exit(1)
else:
    dataset = sys.argv[1]
    dataset_path = sys.argv[2]
    shuffle = sys.argv[3]

posts = []
yO = []
yC = []
yE = []
yA = []
yN = []

print("[LASSO] Loading myPersonality...")
[posts, yO, yC, yE, yA, yN] = dsu.readMyPersonality()
print("[LASSO] Loading embeddings dataset...")
if dataset == 'fasttext':
    transform = True
    wordDictionary = dsu.parseFastText(dataset_path)
else:
    transform = False
    wordDictionary = dsu.loadEmbeddingsDataset(dataset_path)
print("[LASSO] Data successfully loaded.")

filename = "tuning_LASSO_"+dataset

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
    print("[LASSO] Data shuffled.")
else:
    filename = filename + "_noShuffle"

pcc_filename = filename + "_pcc.txt"
filename = filename + ".csv"


#only for test
#subsetSize = len(sumE)
subsetSize = 100
posts = posts[0:subsetSize]
yO = yO[0:subsetSize]
yC = yC[0:subsetSize]
yE = yE[0:subsetSize]
yA = yA[0:subsetSize]
yN = yN[0:subsetSize]

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
conE = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "conc", transform)[0]

print("[LASSO] Word embeddings computed.")

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

l = 1
for labels in [yO, yC, yE, yA, yN]:

    if l==1:
        big5trait = "O"
        print("[LASSO] computing results for Openness...")
    elif l==2:
        big5trait = "C"
        print("[LASSO] computing results for Conscientiousness...")
    elif l==3:
        big5trait = "E"
        print("[LASSO] computing results for Extraversion...")
    elif l==4:
        big5trait = "A"
        print("[LASSO] computing results for Agreeableness...")
    elif l==5:
        big5trait = "N"
        print("[LASSO] computing results for Neuroticism...")
    l += 1

    j = 1
    k_fold = KFold(n_splits=10)
    for data in [sumE, maxE, minE, avgE, conE]:

        if j==1:
            method = "sum"
            print("[LASSO] computing results for sum...")
        elif j==2:
            method = "max"
            print("[LASSO] computing results for max...")
        elif j==3:
            method = "min"
            print("[LASSO] computing results for min...")
        elif j==4:
            method = "avg"
            print("[LASSO] computing results for avg...")
        elif j==5:
            method = "conc"
            print("[LASSO] computing results for concat...")
        j += 1

        #3 error measures
        #10 alpha values - arr[0-9]
        #10 CV iterations - arr[0-9][0-9]
        scores_mse = np.zeros([10,10], dtype=np.float)
        scores_r2 = np.zeros([10,10], dtype=np.float)
        scores_pcc = np.zeros([10,10,2], dtype=np.float) #pcc also has p-value

        i=0
        for train, test in k_fold.split(data):
            print("[LASSO] [CV iteration %d]"%(i+1))
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
            fp.write(big5trait+","+method+",mse,alpha"+str(value+1)+","+str(np.mean(scores_mse[value]))+"\n")
        for value in range(0,len(scores_r2)):
            fp.write(big5trait+","+method+",r2,alpha"+str(value+1)+","+str(np.mean(scores_r2[value]))+"\n")
        for value in range(0,len(scores_pcc)):
            pcc_only = np.array(list(scor[0] for scor in scores_pcc[value])) #extract only pcc score
            pcc_only = pcc_only[np.where(~np.isnan(pcc_only))] #filter out nan values

            if len(pcc_only) != 0:
                mean_score = np.mean(pcc_only)
            else: #all elements are nan
                mean_score = "nan"

            fp.write(big5trait+","+method+",pcc,alpha"+str(value+1)+","+str(mean_score)+"\n")
        fp.close()

        fp = open("Results/"+pcc_filename, "a+")
        for value in range(0,len(scores_pcc)):
            fp.write(big5trait+","+method+",pcc,alpha"+str(value+1)+"\n")
            for elem in scores_pcc[value]:
                fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
            fp.write("\n")
        fp.write("\n\n")
        fp.close()
