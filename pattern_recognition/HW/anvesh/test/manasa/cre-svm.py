import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC

# Load the adultTest dataset from a CSV file
data_set = pd.read_csv('/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/adultTest.csv')

# Extracting Independent and dependent Variables
features = ['age', 'fnlwgt', 'education_num', 'capital_gain', 'capital_loss', 'hours_per_week']
x = data_set[features]
y = data_set['class']

# Encode the target variable
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Splitting the dataset into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Feature Scaling
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Support Vector Classifier
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(x_train, y_train)

# Predicting the test set result
y_pred = classifier.predict(x_test)

# Making the Confusion Matrix
confusion_matrix_result = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print('Confusion matrix is:\n', confusion_matrix_result)
print('The accuracy of SVM is:', accuracy)
print('Classification report is:\n', report)
