# importing libraries  
import numpy as np
import matplotlib.pyplot as mtp  
import pandas as pd  
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

#importing datasets  
data_set= pd.read_csv('D:\TTU SUMMER-1 2023\HW-2\Synthetic_IRIS_Dataset_Ray.csv') 


#Extracting Independent and dependent Variable
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
y=data_set['variety'].astype(str)
features=['sepal.length','sepal.width', 'petal.length', 'petal.width']
x=data_set[features]




# ordinal encode target variable
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
print(x)

# Splitting the dataset into training and test set.  
from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.25, random_state=0)  



#feature Scaling  
from sklearn.preprocessing import StandardScaler    
st_x= StandardScaler()    
x_train= st_x.fit_transform(x_train)    
x_test= st_x.transform(x_test) 



# "Support vector classifier"  
from sklearn.svm import SVC 
classifier = SVC(kernel='linear', random_state=0)  
classifier.fit(x_train, y_train)



#Predicting the test set result  
y_pred= classifier.predict(x_test) 


# Making the Confusion Matrix
Cofusion_Matrix = confusion_matrix(y_test, y_pred)
Accuracy_Score = accuracy_score(y_test, y_pred)
Report = classification_report(y_test, y_pred)

print('Cofusion_matrix is: \n', Cofusion_Matrix)
print('The accuracy of SVM is: ', Accuracy_Score)
print('Classification report is: \n', Report)
