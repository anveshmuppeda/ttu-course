import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load Diabetes Dataset
# url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
path = "/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/pima-indians-diabetes.data.csv"
column_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
# df = pd.read_csv(url, names=column_names)
df = pd.read_csv(path, names=column_names)

# Preprocessing
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Initialize lists to store accuracies
svm_accuracies = []

# Repeat the experiment for 10 iterations
for _ in range(10):
    # Split features and target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Initialize an SVM classifier
    svm_classifier = SVC()

    # Train the SVM classifier
    svm_classifier.fit(X_train, y_train)

    # Predict on the test set
    y_pred = svm_classifier.predict(X_test)

    # Calculate accuracy
    svm_accuracy = accuracy_score(y_test, y_pred)
    svm_accuracies.append(svm_accuracy)

# Compute average accuracy
svm_average_acc = np.mean(svm_accuracies)

# Print average accuracy
print("SVM Average Accuracy:", svm_average_acc)
# 0.7337662337662338

# 10 0.7337662337662338
# 50 0.7337662337662337