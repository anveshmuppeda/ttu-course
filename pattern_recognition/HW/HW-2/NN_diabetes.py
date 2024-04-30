import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

# Load the diabetes dataset
data = pd.read_csv('diabetes.csv')

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, data['Outcome'], test_size=0.2)

# Create a neural network model
model = Sequential()
model.add(Dense(12, activation='relu', input_shape=(8,)))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Train the neural network model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10)

# Evaluate the neural network model on the testing set
score = model.evaluate(X_test, y_test, verbose=0)
print('Test accuracy:', score[1])
