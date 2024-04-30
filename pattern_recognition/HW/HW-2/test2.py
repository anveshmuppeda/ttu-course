import numpy as np
import csv
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Load the Iris dataset
iris = pd.read_csv('D:\TTU SUMMER-1 2023\HW-2\Synthetic_IRIS_Dataset_Ray.csv') 
y=iris.variety

import csv

from csv import reader as csvreader
with open('D:\TTU SUMMER-1 2023\HW-2\Synthetic_IRIS_Dataset_Ray.csv', 'r') as fp:
    reader = csvreader(fp)
    li = list(reader)
X=li

# ordinal encode target variable
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

#print(y)


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the neural network architecture
input_size = X.shape[1]
hidden_size = 10
output_size = y.shape[1]
learning_rate = 0.1
epochs = 500

# Initialize the weights and biases
W1 = np.random.randn(input_size, hidden_size)
b1 = np.zeros(hidden_size)
W2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros(output_size)

# Define the sigmoid activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Define the derivative of the sigmoid function
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Training loop
for epoch in range(epochs):
    # Forward pass
    z1 = np.dot(X_train, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2) + b2
    a2 = sigmoid(z2)
    
    # Backward pass
    delta2 = a2 - y_train
    dW2 = np.dot(a1.T, delta2)
    db2 = np.sum(delta2, axis=0)
    delta1 = np.dot(delta2, W2.T) * sigmoid_derivative(a1)
    dW1 = np.dot(X_train.T, delta1)
    db1 = np.sum(delta1, axis=0)
    
    # Update weights and biases
    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1
    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2

# Forward pass on testing set
z1 = np.dot(X_test, W1) + b1
a1 = sigmoid(z1)
z2 = np.dot(a1, W2) + b2
a2 = sigmoid(z2)

# Convert predicted probabilities to class labels
predicted_labels = np.argmax(a2, axis=1)
true_labels = np.argmax(y_test, axis=1)

# Calculate accuracy
accuracy = np.mean(predicted_labels == true_labels)
print(f'Test Accuracy: {accuracy:.4f}')

