from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras

# Load the Iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Encode the target labels
le = LabelEncoder()
y = le.fit_transform(y)

# Initialize lists to store accuracies
svm_accuracies = []
dnn_accuracies = []

# Repeat the experiment for 50 iterations
for _ in range(5):
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train an SVM classifier
    svm_classifier = svm.SVC()
    svm_classifier.fit(X_train, y_train)
    svm_accuracy = svm_classifier.score(X_test, y_test)
    svm_accuracies.append(svm_accuracy)

    # Train a DNN classifier using Keras
    model = keras.Sequential([
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(3, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, verbose=0)
    dnn_loss, dnn_accuracy = model.evaluate(X_test, y_test)
    dnn_accuracies.append(dnn_accuracy)

# Compute average accuracies
svm_average_acc = np.mean(svm_accuracies)
dnn_average_acc = np.mean(dnn_accuracies)

# Print average accuracies
print("SVM Average Accuracy:", svm_average_acc)
print("DNN Average Accuracy:", dnn_average_acc)
