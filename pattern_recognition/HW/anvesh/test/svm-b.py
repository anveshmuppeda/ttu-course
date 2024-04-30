import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load the dataset
file_path = '/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/linkedin_data.csv'  # Update with your file path
linkedin_df = pd.read_csv(file_path)

# Assuming the last column is the target variable and the rest are features
X = linkedin_df.iloc[:, :-1].values
y = linkedin_df.iloc[:, -1].values

# Encode the target variable
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize and train the SVM classifier
svm_classifier = SVC(kernel='linear', random_state=42)
svm_classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = svm_classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Test Accuracy: {accuracy:.4f}')
