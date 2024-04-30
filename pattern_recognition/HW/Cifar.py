from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import numpy as np
import tensorflow as tf


# Loading the large dataset (e.g., CIFAR-10)
dataset = fetch_openml(name='CIFAR_10', version=1, as_frame=False)
X_data = dataset.data
y_data = dataset.target

# Normalizing the image data
X_data = X_data / 255.0

# Spliting the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=42)

# Initialize lists to store accuracies
svm_accuracies = []
dnn_accuracies = []

# Repeat the experiment for 30 iterations
num_iterations = 1
for _ in range(num_iterations):
    # Train an SVM classifier with a linear kernel
    svm_classifier = SVC(kernel='linear')
    svm_classifier.fit(X_train, y_train)
    svm_predictions = svm_classifier.predict(X_test)
    svm_accuracy = accuracy_score(y_test, svm_predictions)
    svm_accuracies.append(svm_accuracy)

    # Train a DNN classifier using TensorFlow with additional layers and epochs
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=50, verbose=0)
    dnn_predictions = np.argmax(model.predict(X_test), axis=-1)
    dnn_accuracy = accuracy_score(y_test, dnn_predictions)
    dnn_accuracies.append(dnn_accuracy)

# Compute average accuracies
svm_average_acc = np.mean(svm_accuracies)
dnn_average_acc = np.mean(dnn_accuracies)

# Print average accuracies
print("SVM Average Accuracy:", svm_average_acc)
print("DNN Average Accuracy:", dnn_average_acc)
