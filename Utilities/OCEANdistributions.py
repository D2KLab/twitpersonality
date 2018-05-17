import datasetUtils as dsu
import numpy as np
import matplotlib.pyplot as plt

posts = []
yO = []
yC = []
yE = []
yA = []
yN = []

print("[SVM] Loading myPersonality...")
[posts, yO, yC, yE, yA, yN] = dsu.readMyPersonality()

def plotDistribution(x_values, y_values):
    plt.clf()
    plt.plot(x_values, y_values, '.')
    plt.grid()
    plt.show()

xvals = np.linspace(0.0, 5.0, num=101)

for arr in [yO, yC, yE, yA, yN]:
    yvals = [0 for x in range(101)]
    for value in arr:
        index = int(value/0.05)-1
        yvals[index] = yvals[index] + 1
    
    plotDistribution(xvals, yvals)