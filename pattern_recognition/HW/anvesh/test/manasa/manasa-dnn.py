import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

# Load the 1M dataset from a CSV file
data_set = pd.read_csv('/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/LetterRecognition.csv')

# Extracting Independent and dependent Variables
features = ['x.box', 'y.box', 'width', 'high', 'onpix', 'x.bar', 'y.bar', 'x2bar', 'y2bar', 'xybar', 'x2ybr', 'xy2br', 'x.ege', 'xegvy', 'y.ege', 'yegvx']
x = data_set[features]
y = data_set['lettr']

# Encode the target variable
encoder = LabelEncoder()
y = encoder.fit_transform(y)
y = to_categorical(y)  # Convert to one-hot encoded vectors

# Splitting the dataset into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Normalize the input features
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Define the deep learning model
model = Sequential()
model.add(Dense(10, activation='relu', input_shape=(x_train.shape[1],)))
model.add(Dense(10, activation='relu'))
model.add(Dense(y.shape[1], activation='softmax'))  # Output layer with softmax activation for multi-class classification

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=10, batch_size=16, verbose=1)

# Evaluate the model on testing set
_, accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f'Test Accuracy: {accuracy:.4f}')