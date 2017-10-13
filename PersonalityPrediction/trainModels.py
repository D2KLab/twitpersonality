from sklearn.linear_model import LinearRegression
from sklearn import svm

def LReg(data_x, data_y):
    model = LinearRegression().fit(data_x, data_y)
    return [model, "LReg"]

def SVM(data_x, data_y):
    model = svm.SVR().fit(data_x,data_y)
    return [model, "SVM"]
