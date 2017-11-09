from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error
from scipy.stats.stats import pearsonr
import numpy as np
from sklearn.svm import SVR
import datasetUtils as dsu
import embeddings
import sys
import os

def pccMean(arr):
    pcc_only = np.array(list(scor[0] for scor in arr))
    pcc_only = pcc_only[np.where(~np.isnan(pcc_only))]

    if len(pcc_only) != 0:
        mean_score = np.mean(pcc_only)
    else: #all elements are nan
        mean_score = "nan"

    return mean_score

#configs
post_threshold = 3

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

print("[SVM] Loading myPersonality...")
[posts, yO, yC, yE, yA, yN] = dsu.readMyPersonality()
print("[SVM] Loading embeddings dataset...")
if dataset == 'fasttext':
    transform = True
    wordDictionary = dsu.parseFastText(dataset_path)
else:
    transform = False
    wordDictionary = dsu.loadEmbeddingsDataset(dataset_path)
print("[SVM] Data successfully loaded.")

filename = "tuning_SVM_"+dataset

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
    print("[SVM] Data shuffled.")
else:
    filename = filename + "_noShuffle"

pcc_filename = filename + "_pcc.txt"
filename = filename + ".csv"

[sumE, yO, yC, yE, yA, yN]  = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "sum", transform)
maxE = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "max", transform)[0]
minE = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "min", transform)[0]
avgE = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "avg", transform)[0]
conE = embeddings.transformTextForTraining(wordDictionary, post_threshold, posts, old_yO, old_yC, old_yE, old_yA, old_yN, "con", transform)[0]

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
        print("[SVM] computing results for Openness...")
    elif l==2:
        big5trait = "C"
        print("[SVM] computing results for Conscientiousness...")
    elif l==3:
        big5trait = "E"
        print("[SVM] computing results for Extraversion...")
    elif l==4:
        big5trait = "A"
        print("[SVM] computing results for Agreeableness...")
    elif l==5:
        big5trait = "N"
        print("[SVM] computing results for Neuroticism...")
    l += 1

    j = 1
    k_fold = KFold(n_splits=10)
    for data in [sumE, maxE, minE, avgE, conE]:

        if j==1:
            method = "sum"
            print("[SVM] computing results for sum...")
        elif j==2:
            method = "max"
            print("[SVM] computing results for max...")
        elif j==3:
            method = "min"
            print("[SVM] computing results for min...")
        elif j==4:
            method = "avg"
            print("[SVM] computing results for avg...")
        elif j==5:
            method = "conc"
            print("[SVM] computing results for concat...")
        j += 1

        linear = np.zeros([3,10,2], dtype=np.float)
        poly_c1_d2 = np.zeros([3,10,2], dtype=np.float)
        poly_c10_d2 = np.zeros([3,10,2], dtype=np.float)
        poly_c100_d2 = np.zeros([3,10,2], dtype=np.float)
        poly_c1_d3 = np.zeros([3,10,2], dtype=np.float)
        poly_c10_d3 = np.zeros([3,10,2], dtype=np.float)
        poly_c100_d3 = np.zeros([3,10,2], dtype=np.float)
        rbf_g001_c1 = np.zeros([3,10,2], dtype=np.float)
        rbf_g001_c10 = np.zeros([3,10,2], dtype=np.float)
        rbf_g001_c100 = np.zeros([3,10,2], dtype=np.float)
        rbf_g01_c1 = np.zeros([3,10,2], dtype=np.float)
        rbf_g01_c10 = np.zeros([3,10,2], dtype=np.float)
        rbf_g01_c100 = np.zeros([3,10,2], dtype=np.float)
        rbf_g1_c1 = np.zeros([3,10,2], dtype=np.float)
        rbf_g1_c10 = np.zeros([3,10,2], dtype=np.float)
        rbf_g1_c100 = np.zeros([3,10,2], dtype=np.float)
        rbf_g10_c1 = np.zeros([3,10,2], dtype=np.float)
        rbf_g10_c10 = np.zeros([3,10,2], dtype=np.float)
        rbf_g10_c100 = np.zeros([3,10,2], dtype=np.float)

        i=1
        for train, test in k_fold.split(data):
            print("[SVM] [CV iteration %d]"%i)
            model = SVR(kernel='linear', C=1).fit(data[train],labels[train])
            res = model.predict(data[test])
            linear[0][i-1] = (mean_squared_error(labels[test],res))
            linear[1][i-1] = (model.score(data[test], labels[test]))
            linear[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            #print(pearsonr(res, labels[test]))

            model = SVR(kernel='poly', degree=2, C=1).fit(data[train],labels[train])
            res = model.predict(data[test])
            poly_c1_d2[0][i-1] = (mean_squared_error(labels[test],res))
            poly_c1_d2[1][i-1] = (model.score(data[test], labels[test]))
            poly_c1_d2[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='poly', degree=2, C=10).fit(data[train],labels[train])
            res = model.predict(data[test])
            poly_c10_d2[0][i-1] = (mean_squared_error(labels[test],res))
            poly_c10_d2[1][i-1] = (model.score(data[test], labels[test]))
            poly_c10_d2[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='poly', degree=2, C=100).fit(data[train],labels[train])
            res = model.predict(data[test])
            poly_c100_d2[0][i-1] = (mean_squared_error(labels[test],res))
            poly_c100_d2[1][i-1] = (model.score(data[test], labels[test]))
            poly_c100_d2[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='poly', degree=3, C=1).fit(data[train],labels[train])
            res = model.predict(data[test])
            poly_c1_d3[0][i-1] = (mean_squared_error(labels[test],res))
            poly_c1_d3[1][i-1] = (model.score(data[test], labels[test]))
            poly_c1_d3[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='poly', degree=3, C=10).fit(data[train],labels[train])
            res = model.predict(data[test])
            poly_c10_d3[0][i-1] = (mean_squared_error(labels[test],res))
            poly_c10_d3[1][i-1] = (model.score(data[test], labels[test]))
            poly_c10_d3[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='poly', degree=3, C=100).fit(data[train],labels[train])
            res = model.predict(data[test])
            poly_c100_d3[0][i-1] = (mean_squared_error(labels[test],res))
            poly_c100_d3[1][i-1] = (model.score(data[test], labels[test]))
            poly_c100_d3[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=0.01, C=1).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g001_c1[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g001_c1[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g001_c1[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=0.01, C=10).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g001_c10[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g001_c10[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g001_c10[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=0.01, C=100).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g001_c100[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g001_c100[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g001_c100[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=0.1, C=1).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g01_c1[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g01_c1[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g01_c1[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=0.1, C=10).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g01_c10[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g01_c10[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g01_c10[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=0.1, C=100).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g01_c100[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g01_c100[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g01_c100[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=1, C=1).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g1_c1[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g1_c1[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g1_c1[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=1, C=10).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g1_c10[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g1_c10[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g1_c10[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=1, C=100).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g1_c100[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g1_c100[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g1_c100[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=10, C=1).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g10_c1[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g10_c1[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g10_c1[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=10, C=10).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g10_c10[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g10_c10[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g10_c10[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            model = SVR(kernel='rbf', gamma=10, C=100).fit(data[train],labels[train])
            res = model.predict(data[test])
            rbf_g10_c100[0][i-1] = (mean_squared_error(labels[test],res))
            rbf_g10_c100[1][i-1] = (model.score(data[test], labels[test]))
            rbf_g10_c100[2][i-1] = (pearsonr(model.predict(data[test]), labels[test]))

            i += 1

        fp = open("Results/"+filename, "a+")
        fp.write(big5trait+","+method+",mse,linear,1,,,"+str(np.mean(linear[0]))+"\n")
        fp.write(big5trait+","+method+",r2,linear,1,,,"+str(np.mean(linear[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,linear,1,,,"+str(pccMean(linear[2]))+"\n")
        fp.write(big5trait+","+method+",mse,poly,1,,2,"+str(np.mean(poly_c1_d2[0]))+"\n")
        fp.write(big5trait+","+method+",r2,poly,1,,2,"+str(np.mean(poly_c1_d2[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,poly,1,,2,"+str(pccMean(poly_c1_d2[2]))+"\n")
        fp.write(big5trait+","+method+",mse,poly,10,,2,"+str(np.mean(poly_c10_d2[0]))+"\n")
        fp.write(big5trait+","+method+",r2,poly,10,,2,"+str(np.mean(poly_c10_d2[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,poly,10,,2,"+str(pccMean(poly_c10_d2[2]))+"\n")
        fp.write(big5trait+","+method+",mse,poly,100,,2,"+str(np.mean(poly_c100_d2[0]))+"\n")
        fp.write(big5trait+","+method+",r2,poly,100,,2,"+str(np.mean(poly_c100_d2[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,poly,100,,2,"+str(pccMean(poly_c100_d2[2]))+"\n")
        fp.write(big5trait+","+method+",mse,poly,1,,3,"+str(np.mean(poly_c1_d3[0]))+"\n")
        fp.write(big5trait+","+method+",r2,poly,1,,3,"+str(np.mean(poly_c1_d3[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,poly,1,,3,"+str(pccMean(poly_c1_d3[2]))+"\n")
        fp.write(big5trait+","+method+",mse,poly,10,,3,"+str(np.mean(poly_c10_d3[0]))+"\n")
        fp.write(big5trait+","+method+",r2,poly,10,,3,"+str(np.mean(poly_c10_d3[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,poly,10,,3,"+str(pccMean(poly_c10_d3[2]))+"\n")
        fp.write(big5trait+","+method+",mse,poly,100,,3,"+str(np.mean(poly_c100_d3[0]))+"\n")
        fp.write(big5trait+","+method+",r2,poly,100,,3,"+str(np.mean(poly_c100_d3[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,poly,100,,3,"+str(pccMean(poly_c100_d3[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,1,0.01,,"+str(np.mean(rbf_g001_c1[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,1,0.01,,"+str(np.mean(rbf_g001_c1[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,1,0.01,,"+str(pccMean(rbf_g001_c1[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,10,0.01,,"+str(np.mean(rbf_g001_c10[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,10,0.01,,"+str(np.mean(rbf_g001_c10[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,10,0.01,,"+str(pccMean(rbf_g001_c10[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,100,0.01,,"+str(np.mean(rbf_g001_c100[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,100,0.01,,"+str(np.mean(rbf_g001_c100[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,100,0.01,,"+str(pccMean(rbf_g001_c100[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,1,0.1,,"+str(np.mean(rbf_g01_c1[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,1,0.1,,"+str(np.mean(rbf_g01_c1[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,1,0.1,,"+str(pccMean(rbf_g01_c1[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,10,0.1,,"+str(np.mean(rbf_g01_c10[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,10,0.1,,"+str(np.mean(rbf_g01_c10[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,10,0.1,,"+str(pccMean(rbf_g01_c10[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,100,0.1,,"+str(np.mean(rbf_g01_c100[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,100,0.1,,"+str(np.mean(rbf_g01_c100[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,100,0.1,,"+str(pccMean(rbf_g01_c100[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,1,1,,"+str(np.mean(rbf_g1_c1[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,1,1,,"+str(np.mean(rbf_g1_c1[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,1,1,,"+str(pccMean(rbf_g1_c1[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,10,1,,"+str(np.mean(rbf_g1_c10[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,10,1,,"+str(np.mean(rbf_g1_c10[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,10,1,,"+str(pccMean(rbf_g1_c10[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,100,1,,"+str(np.mean(rbf_g1_c100[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,100,1,,"+str(np.mean(rbf_g1_c100[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,100,1,,"+str(pccMean(rbf_g1_c100[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,1,10,,"+str(np.mean(rbf_g10_c1[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,1,10,,"+str(np.mean(rbf_g10_c1[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,1,10,,"+str(pccMean(rbf_g10_c1[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,10,10,,"+str(np.mean(rbf_g10_c10[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,10,10,,"+str(np.mean(rbf_g10_c10[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,10,10,,"+str(pccMean(rbf_g10_c10[2]))+"\n")
        fp.write(big5trait+","+method+",mse,rbf,100,10,,"+str(np.mean(rbf_g10_c100[0]))+"\n")
        fp.write(big5trait+","+method+",r2,rbf,100,10,,"+str(np.mean(rbf_g10_c100[1]))+"\n")
        fp.write(big5trait+","+method+",pcc,rbf,100,10,,"+str(pccMean(rbf_g10_c100[2]))+"\n")
        fp.close()

        #print (linear[2])

        #input()

        fp = open("Results/"+pcc_filename, "a+")
        fp.write(big5trait+","+method+",pcc,linear,1,,\n")
        for elem in linear[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,poly,1,,2\n")
        for elem in poly_c1_d2[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,poly,10,,2\n")
        for elem in poly_c10_d2[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,poly,100,,2\n")
        for elem in poly_c100_d2[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,poly,1,,3\n")
        for elem in poly_c1_d3[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,poly,10,,3\n")
        for elem in poly_c10_d3[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,poly,100,,3\n")
        for elem in poly_c100_d3[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,1,0.01,\n")
        for elem in rbf_g001_c1[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,10,0.01,\n")
        for elem in rbf_g001_c10[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,100,0.01,\n")
        for elem in rbf_g001_c100[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,1,0.1,\n")
        for elem in rbf_g01_c1[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,10,0.1,\n")
        for elem in rbf_g01_c10[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,100,0.1,\n")
        for elem in rbf_g01_c100[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,1,1,\n")
        for elem in rbf_g1_c1[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,10,1,\n")
        for elem in rbf_g1_c10[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,100,1,\n")
        for elem in rbf_g1_c100[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,1,10,\n")
        for elem in rbf_g10_c1[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,10,10,\n")
        for elem in rbf_g10_c10[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.write(big5trait+","+method+",pcc,rbf,100,10,\n")
        for elem in rbf_g10_c100[2]:
            fp.write(str(elem[0])+"\t"+str(elem[1])+"\n")
        fp.write("\n")
        fp.close()
