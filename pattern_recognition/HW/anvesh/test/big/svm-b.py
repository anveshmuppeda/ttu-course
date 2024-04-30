import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Load the dataset
data_set = pd.read_csv('/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/2M.csv')  # Replace '/path/to/1M.csv' with the actual path to your dataset

# Extracting Independent and dependent Variable
X = data_set.iloc[:, :-1].values
y = data_set.iloc[:, -1].values

# Splitting the dataset into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Feature Scaling
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

# Support vector classifier
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(X_train, y_train)

# Predicting the test set result
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
confusion_Matrix = confusion_matrix(y_test, y_pred)
accuracy_Score = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print('Confusion Matrix is: \n', confusion_Matrix)
print('The accuracy of SVM is: ', accuracy_Score)
print('Classification report is: \n', report)
