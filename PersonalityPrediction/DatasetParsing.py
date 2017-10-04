import os

#9913 lines
##AUTHID,"STATUS","sEXT","sNEU","sAGR","sCON","sOPN","cEXT","cNEU","cAGR","cCON","cOPN","DATE","NETWORKSIZE","BETWEENNESS","NBETWEENNESS","DENSITY","BROKERAGE","NBROKERAGE","TRANSITIVITY"

data = []
y_O = []
y_C = []
y_E = []
y_A = []
y_N = []

#parse the dataset file one line at a time
for line in open("Dataset/mypersonality_final.csv", "r"):
    user_id = line.split(',')[0][1:]
    status = line.split(user_id)[1][3:].split('"",')[0]
    big5 = line.split(status)[1][3:].split(',""')[0].split(",")

    data.append(status)
    y_E.append(big5[0])
    y_N.append(big5[1])
    y_A.append(big5[2])
    y_C.append(big5[3])
    y_O.append(big5[4])

if not os.path.exists("Dataset"):
    os.makedirs("Dataset")

fp = open("Dataset/statuses.txt", "w")
for status in data:
    fp.write(status+"\n")
fp.close()
fp = open("Dataset/big5labels.txt", "w")
for i in range(0,len(data)):
    fp.write(str(y_O[i])+" "+y_C[i]+" "+y_E[i]+" "+y_A[i]+" "+y_N[i]+"\n")
fp.close()

print("Files written.")
