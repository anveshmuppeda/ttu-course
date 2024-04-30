# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 19:19:29 2023

@author: vishw
"""
import psutil
import time
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import memory_profiler as mp

wine = datasets.load_wine()
X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


svm_cpu_start = psutil.cpu_percent()
model_SVM_start = time.time()
svm = SVC()
svm.fit(X_train, y_train)
y_pred = svm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
model_SVM_training_time = time.time() - model_SVM_start
model_SVM_memory_usage = mp.memory_usage((SVC().fit, (X_train, y_train)))
# End measuring CPU utilization
SVC_cpu_utilization_end = psutil.cpu_percent()

print("SVM Accuracy:", round(accuracy*100,2))
print("Training Time:", round(model_SVM_training_time, 3),"seconds")
print("Memory Usage:", round(np.max(model_SVM_memory_usage), 3), "MB")
print("CPU Utilization:", round(SVC_cpu_utilization_end - svm_cpu_start, 2), "%\n")