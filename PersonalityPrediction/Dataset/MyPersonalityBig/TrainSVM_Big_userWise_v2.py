from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
from sklearn.svm import SVR
import numpy as np

#configs
x_scale = (0,5.5)
y_scale = (0,5.5)

def savePlot(y_true, y_pred, title, path):
    plt.clf()
    plt.xlim(x_scale)
    plt.ylim(y_scale)
    plt.plot(y_true, y_pred, '.')
    plt.ylabel('predicted values('+str(len(y_true))+")")
    plt.xlabel('actual values('+str(len(y_true))+")")
    plt.title(title)
    plt.savefig(path)

training_samples = []
yO = []
yC = []
yE = []
yA = []
yN = []

for line in open("users_embeddings.csv","r"):
    parts = line[:-1].split(",")
    yO.append(float(parts[1]))
    yC.append(float(parts[2]))
    yE.append(float(parts[3]))
    yA.append(float(parts[4]))
    yN.append(float(parts[5]))
    embed = np.array(list(float(elem) for elem in parts[6:]),dtype=float)
    training_samples.append(embed)

training_samples = np.array(training_samples)
yO = np.array(yO)
yC = np.array(yC)
yE = np.array(yE)
yA = np.array(yA)
yN = np.array(yN)
print("Training set loaded. Total samples:",len(training_samples))

#shuffle data
s = np.arange(training_samples.shape[0])
np.random.shuffle(s)
training_samples = training_samples[s]
yO = yO[s]
yC = yC[s]
yE = yE[s]
yA = yA[s]
yN = yN[s]
print("Data shuffled.")

for users_subset in [5000,7500,10000,12500,15000,17500,20000]:

    training_samples_sub = training_samples[0:users_subset]
    yO_sub = yO[0:users_subset]
    yC_sub = yC[0:users_subset]
    yE_sub = yE[0:users_subset]
    yA_sub = yA[0:users_subset]
    yN_sub = yN[0:users_subset]

    print("\nUsers subset:",users_subset)

    trait = 1
    k_fold = KFold(n_splits=4)
    for labels in [yO_sub, yC_sub, yE_sub, yA_sub, yN_sub]:

        if trait==1:
            big5trait = "O"
            gamma = 1
            C = 1
            print("\tTraining model for Openness...")
        elif trait==2:
            big5trait = "C"
            gamma = 1
            C = 1
            print("\tTraining model for Conscientiousness...")
        elif trait==3:
            big5trait = "E"
            gamma = 1
            C = 10
            print("\tTraining model for Extraversion...")
        elif trait==4:
            big5trait = "A"
            gamma = 1
            C = 1
            print("\tTraining model for Agreeableness...")
        elif trait==5:
            big5trait = "N"
            gamma = 10
            C = 10
            print("\tTraining model for Neuroticism...")
        trait += 1

        mses = []

        it = 1
        for train, test in k_fold.split(training_samples_sub):
            print("\t\tcv iteration",it)
            model = SVR(kernel='rbf', gamma = gamma, C=C).fit(training_samples_sub[train],labels[train])
            res = model.predict(training_samples_sub[test])
            mse = mean_squared_error(res, labels[test])
            mses.append(mse)

            title = big5trait+"_"+str(users_subset)+"_cv"+str(it)+",\n"+str(round(mse,4))[0:5]
            savePlot(labels[test],res, title, "Plots/SVM_Big_UserWise_v2/"+title.split("\n")[0]+".png")
            it+=1

        with open("MPBig_results_userWise_v2.csv", "a") as outfile:
            outfile.write(big5trait+","+str(users_subset)+","+str(len(training_samples[train]))+","+str(np.mean(np.array(mses)))+"\n")
