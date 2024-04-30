import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense

# Load the dataset from a pima-indians-diabetes.data.csv file
data_set = pd.read_csv('/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/pima-indians-diabetes.data.csv', header=None)

# Extracting Independent and dependent Variables
X = data_set.iloc[:, :-1].values  # Independent variables
y = data_set.iloc[:, -1].values  # Dependent variable (target)

# Splitting the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # Scale the training data
X_test = scaler.transform(X_test)  # Scale the test data using the same scaler

# Define the deep learning model
model = Sequential()
model.add(Dense(10, activation='relu', input_shape=(X_train.shape[1],)))  # Input layer with 10 neurons and ReLU activation
model.add(Dense(10, activation='relu'))  # Hidden layer with 10 neurons and ReLU activation
model.add(Dense(1, activation='sigmoid'))  # Output layer for binary classification with sigmoid activation

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=1000, batch_size=16, verbose=1)  # Train the model for 1000 epochs with a batch size of 16

# Evaluate the model on training set
_, train_accuracy = model.evaluate(X_train, y_train, verbose=0)  # Evaluate the model's performance on the training data
print(f'Train Accuracy: {train_accuracy:.4f}')  # Print the training accuracy

# Evaluate the model on testing set
_, accuracy = model.evaluate(X_test, y_test, verbose=0)  # Evaluate the model's performance on the test data
print(f'Test Accuracy: {accuracy:.4f}')  # Print the test accuracy
