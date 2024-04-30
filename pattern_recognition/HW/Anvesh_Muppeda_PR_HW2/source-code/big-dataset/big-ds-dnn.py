import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

# Load the dataset from a Churn_Modelling.csv file
data_set = pd.read_csv('/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/Churn_Modelling.csv')

# Extracting Independent and dependent Variables
features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
x = data_set[features]  # Independent variables
y = data_set['Exited']  # Dependent variable (target)

# Encode the target variable
encoder = LabelEncoder()
y = encoder.fit_transform(y)    # Encode 'Exited' column to numerical values
y = to_categorical(y)  # Convert numerical labels to one-hot encoded vectors

# Splitting the dataset into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Normalize the input features
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Define the deep learning model
model = Sequential()
# Add input layer with 10 neurons and ReLU activation
model.add(Dense(10, activation='relu', input_shape=(x_train.shape[1],)))
# Add hidden layer with 10 neurons and ReLU activation
model.add(Dense(10, activation='relu'))
# Add output layer with 2 neurons for binary classification (Exited or not), using softmax activation
model.add(Dense(2, activation='softmax')) 

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
# Train the model for 10 epochs with a batch size of 16
model.fit(x_train, y_train, epochs=10, batch_size=16, verbose=1)

# Evaluate the model on testing set
# Evaluate the model's performance on the test data
_, accuracy = model.evaluate(x_test, y_test, verbose=0)
# Print the test accuracy
print(f'Test Accuracy: {accuracy:.4f}')