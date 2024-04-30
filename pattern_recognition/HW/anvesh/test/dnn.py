import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras

# Load Diabetes Dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
column_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
# df = pd.read_csv(url, names=column_names)

path = "/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/pima-indians-diabetes.data.csv"
df = pd.read_csv(path, names=column_names)

# Preprocessing
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Initialize lists to store accuracies
dnn_accuracies = []

# Repeat the experiment for 10 iterations
for _ in range(5):
    # Split features and target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Initialize a DNN model
    model = keras.Sequential([
        keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    # Evaluate the model on the test set
    _, dnn_accuracy = model.evaluate(X_test, y_test, verbose=0)
    dnn_accuracies.append(dnn_accuracy)

# Compute average accuracy
dnn_average_acc = np.mean(dnn_accuracies)

# Print average accuracy
print("DNN Average Accuracy:", dnn_average_acc)