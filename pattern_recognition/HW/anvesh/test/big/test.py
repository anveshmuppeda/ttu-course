import numpy as np
import matplotlib.pyplot as mtp  
import pandas as pd  
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC 

# Read the CSV file
data_set = pd.read_csv('/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/anvesh/test/dataset/1M.csv') 

# Assuming 'col10' is the target variable, update as needed
y = data_set['col10'].astype(str)
features = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9']
x = data_set[features]

# Splitting the dataset into training and test set.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Feature Scaling
st_x = StandardScaler()
x_train = st_x.fit_transform(x_train)
x_test = st_x.transform(x_test)

# Support Vector Classifier
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(x_train, y_train)

# Predicting the test set result
y_pred = classifier.predict(x_test)

# Making the Confusion Matrix
Cofusion_Matrix = confusion_matrix(y_test, y_pred)
Accuracy_Score = accuracy_score(y_test, y_pred)
Report = classification_report(y_test, y_pred)

print('Cofusion_matrix is: \n', Cofusion_Matrix)
print('The accuracy of SVM is: ', Accuracy_Score)
print('Classification report is: \n', Report)
