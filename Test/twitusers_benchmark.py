from sklearn.metrics import mean_squared_error
from pathlib import Path
import numpy as np
import embeddings
import sys
import os

#true values
O = []
C = []
E = []
A = []
N = []
#predicted with method 1
O1 = []
C1 = []
E1 = []
A1 = []
N1 = []
#predicted with method 2
O2 = []
C2 = []
E2 = []
A2 = []
N2 = []

for line in open("questionnaires.csv", "r"):
    parts= line.split(";")
    O.append(float(parts[-10].replace(",",".")))
    C.append(float(parts[-9].replace(",",".")))
    E.append(float(parts[-8].replace(",",".")))
    A.append(float(parts[-7].replace(",",".")))
    N.append(float(parts[-6].replace(",",".")))

for line in open("Data/personality_predictions1.csv"):
    parts = line.split(",")
    O1.append(float(parts[1].replace(",",".")))
    C1.append(float(parts[2].replace(",",".")))
    E1.append(float(parts[3].replace(",",".")))
    A1.append(float(parts[4].replace(",",".")))
    N1.append(float(parts[5].replace(",",".")))


for line in open("Data/personality_predictions2.csv"):
    parts = line.split(",")
    O2.append(float(parts[1].replace(",",".")))
    C2.append(float(parts[2].replace(",",".")))
    E2.append(float(parts[3].replace(",",".")))
    A2.append(float(parts[4].replace(",",".")))
    N2.append(float(parts[5].replace(",",".")))

mse_O_1 = mean_squared_error(O,O1)
mse_C_1 = mean_squared_error(C,C1)
mse_E_1 = mean_squared_error(E,E1)
mse_A_1 = mean_squared_error(A,A1)
mse_N_1 = mean_squared_error(N,N1)

mse_O_2 = mean_squared_error(O,O2)
mse_C_2 = mean_squared_error(C,C2)
mse_E_2 = mean_squared_error(E,E2)
mse_A_2 = mean_squared_error(A,A2)
mse_N_2 = mean_squared_error(N,N2)

fp = open("twitusers_predictions_benchmark.csv", "w")
fp.write("mse,O,1,"+str(mse_O_1)+"\n")
fp.write("mse,C,1,"+str(mse_C_1)+"\n")
fp.write("mse,E,1,"+str(mse_E_1)+"\n")
fp.write("mse,A,1,"+str(mse_A_1)+"\n")
fp.write("mse,N,1,"+str(mse_N_1)+"\n")
fp.write("mse,O,2,"+str(mse_O_2)+"\n")
fp.write("mse,C,2,"+str(mse_C_2)+"\n")
fp.write("mse,E,2,"+str(mse_E_2)+"\n")
fp.write("mse,A,2,"+str(mse_A_2)+"\n")
fp.write("mse,N,2,"+str(mse_N_2)+"\n")
fp.close()