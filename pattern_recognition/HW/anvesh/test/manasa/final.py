import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.impute import SimpleImputer

# Load the dataset from a CSV file
data_set = pd.read_csv('/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/Churn_Modelling_m.csv')

# Extracting Independent and dependent Variables
features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
x = data_set[features]
y = data_set['Exited']

# Splitting the dataset into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Impute missing values in the dataset
imputer = SimpleImputer(strategy='mean')
x_train_imputed = imputer.fit_transform(x_train)
x_test_imputed = imputer.transform(x_test)

# Feature Scaling
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train_imputed)
x_test_scaled = scaler.transform(x_test_imputed)

# Support Vector Classifier
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(x_train_scaled, y_train)

# Predicting the test set result
y_pred = classifier.predict(x_test_scaled)

# Making the Confusion Matrix
confusion_matrix_result = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print('Confusion matrix is:\n', confusion_matrix_result)
print('The accuracy of SVM is:', accuracy)
print('Classification report is:\n', report)
