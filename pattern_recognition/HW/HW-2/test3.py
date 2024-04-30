import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the Iris dataset from a CSV file
iris_df = pd.read_csv('D:\TTU SUMMER-1 2023\HW-2\Synthetic_IRIS_Dataset_Ray.csv')

#Extracting Independent and dependent Variable
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
y=iris_df['variety'].astype(str)
features=['sepal.length','sepal.width', 'petal.length', 'petal.width']
x=iris_df[features]




# ordinal encode target variable
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Normalize the input features
X_train = (X_train - np.mean(X_train, axis=0)) / np.std(X_train, axis=0)
X_test = (X_test - np.mean(X_test, axis=0)) / np.std(X_test, axis=0)

# Define the neural network architecture
input_size = X_train.shape[1]
hidden_size = 10
output_size = np.max(y_train) + 1
learning_rate = 0.1
epochs = 5000

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
    
    # Calculate the loss
    loss = np.mean((a2 - y_train.reshape(-1, 1)) ** 2)
    
    # Backward pass
    delta2 = (a2 - y_train.reshape(-1, 1)) * sigmoid_derivative(z2)
    dW2 = np.dot(a1.T, delta2)
    db2 = np.sum(delta2, axis=0)
    delta1 = np.dot(delta2, W2.T) * sigmoid_derivative(z1)
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

# Convert the predicted probabilities to class labels
predictions = np.argmax(a2, axis=1)

# Calculate the accuracy on testing set
accuracy = np.mean(predictions == y_test)
print(f'Test Accuracy: {accuracy:.4f}')
