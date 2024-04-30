import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

# Load the dataset from a pima-indians-diabetes.data.csv file
file_path = '/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/pima-indians-diabetes.data.csv' 
diabetes_df = pd.read_csv(file_path)

# Extract the input features and target variable
X = diabetes_df.iloc[:, :-1].values # Independent variables
y = diabetes_df.iloc[:, -1].values   # Dependent variable (target)

# Encode the target variable
encoder = LabelEncoder()
y = encoder.fit_transform(y)    # Encode 'Exited' column to numerical values
y = to_categorical(y)  # Convert to one-hot encoded vectors

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # Scale the training data
X_test = scaler.transform(X_test)    # Scale the test data using the same scaler

# Define the deep learning model
model = Sequential()
# Add input layer with 10 neurons and ReLU activation
model.add(Dense(10, activation='relu', input_shape=(X_train.shape[1],)))
# Add hidden layer with 10 neurons and ReLU activation
model.add(Dense(10, activation='relu'))
# Add output layer with 2 neurons for binary classification (Exited or not), using softmax activation
model.add(Dense(y_train.shape[1], activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
# Train the model for 10 epochs with a batch size of 16
model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=1)

# Evaluate the model on testing set
# Evaluate the model's performance on the test data
_, accuracy = model.evaluate(X_test, y_test, verbose=0)
# Print the test accuracy
print(f'Test Accuracy: {accuracy:.4f}')
