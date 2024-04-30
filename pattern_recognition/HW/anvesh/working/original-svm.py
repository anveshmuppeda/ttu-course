import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load Adult dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
column_names = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']
df = pd.read_csv(url, names=column_names, na_values=' ?', skipinitialspace=True)

# Drop rows with missing values
df.dropna(inplace=True)

# Encode categorical variables
categorical_cols = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country', 'income']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Split features and target
X = df.drop('income', axis=1)
y = df['income']

# Standardize features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Initialize list to store accuracies
svm_accuracies = []

# Repeat the experiment for 50 iterations
for _ in range(5):
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train an SVM classifier
    svm_classifier = SVC()
    svm_classifier.fit(X_train, y_train)
    svm_accuracy = accuracy_score(y_test, svm_classifier.predict(X_test))
    svm_accuracies.append(svm_accuracy)

# Compute average accuracy
svm_average_acc = np.mean(svm_accuracies)

# Print average accuracy
print("SVM Average Accuracy:", svm_average_acc)
