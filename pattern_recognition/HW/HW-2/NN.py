"""
@author: Akdeniz Kutay Ocal
Title: ANN on Iris Dataset
"""

import numpy as np
from sklearn import datasets
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.metrics as mt


def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))


def sigmoid_derivative(z):
    return z * (1.0 - z)


class NeuralNetwork:
    def __init__(self, inSize, sl2, clsSize, lrt):

        self.iSz = inSize
        self.oSz = clsSize
        self.hSz = sl2
        self.weights1 = (np.random.rand(self.hSz, self.iSz + 1) - 0.5) / np.sqrt(self.iSz)
        self.weights2 = (np.random.rand(self.oSz, self.hSz + 1) - 0.5) / np.sqrt(self.hSz)

        self.output = 0
        self.layer1 = np.zeros(self.hSz)
        self.eta = lrt

    def feedforward(self, x):
        x_c = np.r_[1, x]
        self.layer1 = sigmoid(np.dot(self.weights1, x_c))
        layer1_c = np.r_[1, self.layer1]
        self.output = sigmoid(np.dot(self.weights2, layer1_c))

    def backprop(self, x, trg):

        sigma_3 = (trg - self.output)  # outer layer error
        sigma_3 = np.reshape(sigma_3, (self.oSz, 1))

        layer1_c = np.r_[1, self.layer1]  # hidden layer activations+bias
        sigma_2 = np.dot(self.weights2.T, sigma_3)
        tmp = sigmoid_derivative(layer1_c)
        tmp = np.reshape(tmp, (self.hSz + 1, 1))
        sigma_2 = np.multiply(sigma_2, tmp)  # hidden layer error
        delta2 = sigma_3 * layer1_c  # weights2 update

        x_c = np.r_[1, x]  # input layer +bias
        delta1 = sigma_2[1:, ] * x_c  # weights1 update

        return delta1, delta2

    def fit(self, X, y, iterNo):

        m = np.shape(X)[0]
        for i in range(iterNo):
            D1 = np.zeros(np.shape(self.weights1))
            D2 = np.zeros(np.shape(self.weights2))
            for j in range(m):
                self.feedforward(X[j])
                [delta1, delta2] = self.backprop(X[j], y[j])
                D1 = D1 + delta1
                D2 = D2 + delta2
            self.weights1 = self.weights1 + self.eta * (D1 / m)
            self.weights2 = self.weights2 + self.eta * (D2 / m)

    def predict(self, X):

        m = np.shape(X)[0]

        y = np.zeros((m, 3))

        for i in range(m):
            self.feedforward(X[i])
            y[i] = self.output
        return y


# Loading the data
iris = datasets.load_iris()
print("hi")
X = iris.data

# Formatting the Y so that it is 150x3
Y = np.zeros((150, 3))
for i in range(150):
    Y[i][iris.target[i]] = 1

# Shuffling the data
order = range(np.shape(iris.data)[0])
allocation = list(order)
np.random.shuffle(allocation)

# Splitting Data
x_train = [iris.data[allocation[i]].tolist() for i in range(100)]
y_train = [Y[allocation[i]] for i in range(100)]

x_val = [iris.data[allocation[i]].tolist() for i in range(100, 125)]
y_val = [Y[allocation[i]] for i in range(100, 125)]

x_test = [iris.data[allocation[i]].tolist() for i in range(125, 150)]
y_test = [Y[allocation[i]] for i in range(125, 150)]
test_target = [iris.target[allocation[i]] for i in range(125, 150)]


# Finding the best model that predicts validation sets

# Generating model list
nnList = []
for i in range(10):
    nn = NeuralNetwork(4, 6, 3, 0.2)
    nn.fit(x_train, y_train, 1000)
    nnList.append(nn)

# Finding the best model

bestIndex = float('-inf')
highest_error = float('inf')

for i, nn in enumerate(nnList):
    y_predict = nn.predict(x_val)
    error = mean_squared_error(y_val, y_predict)
    if highest_error > error:
        bestIndex = i
        highest_error = error
    print("Epoch ", i, "error rate:", error, sep=" ")


y_predict = nnList[bestIndex].predict(x_test)
error = mean_squared_error(y_test, y_predict)

# Turning prediction list to target list
# From 25x3 to 25 that has values between 0-2
labels = []
bestOutput = float('-inf')
index = float('-inf')

for i in range(np.shape(y_predict)[0]):
    for j in range(3):
        if y_predict[i][j] > bestOutput:
            bestOutput = y_predict[i][j]
            index = j
    bestOutput = float('-inf')
    labels.append(index)

# Printing accuracy
print("Accuracy: ", mt.accuracy_score(test_target, labels))

# Plotting confusion matrix
plt.xlabel("True label")
plt.ylabel("Predicted label")
plt.subplots(figsize=(8, 8))

cm = confusion_matrix(test_target, labels)
sns.heatmap(cm.T, square=True, annot=True, fmt='d', cbar=False, xticklabels=iris.target_names,
            yticklabels=iris.target_names)

plt.show()
