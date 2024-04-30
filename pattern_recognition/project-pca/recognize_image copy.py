import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import cv2
import zipfile

# Function to load face images from a zip file
def load_face_images(zipfile_path):
    faces = {}
    with zipfile.ZipFile(zipfile_path) as facezip:
        for filename in facezip.namelist():
            # Check if the file is a JPG image
            if not filename.endswith(".jpg"):
                continue
            # Read the image from the zip file
            with facezip.open(filename) as image:
                # Decode the image and store it in grayscale
                faces[filename] = cv2.imdecode(np.frombuffer(
                    image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    return faces

# Function to extract information about a person from the filename
def extract_person_info(filename):
    # Remove the prefix and split the filename
    filename = filename.replace("Grp13Person", "").split("/")
    # Extract the person number and image number
    person_num = int(filename[0])
    img_num = int(filename[1].split("_")[0]) % 10
    return (person_num, img_num)

# Function to split the data into training and testing sets
def split_data(zipfilepath):
    training_data = {}
    testing_data = {}
    with zipfile.ZipFile(zipfilepath) as facezip:
        for filename in facezip.namelist():
            # Check if the file is a JPG image
            if not filename.endswith(".jpg"):
                continue
            # Extract information about the person from the filename
            person_num, img_num = extract_person_info(filename=filename)
            # Assign images to training or testing set based on the image number
            if img_num == 0 or img_num == 1:
                # Add the image to the testing set
                with facezip.open(filename) as image:
                    testing_data[filename] = cv2.imdecode(np.frombuffer(
                        image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            else:
                # Add the image to the training set
                with facezip.open(filename) as image:
                    training_data[filename] = cv2.imdecode(np.frombuffer(
                        image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    return training_data, testing_data

# Function to calculate prediction statistics
def calculate_statistics(correct_predictions, wrong_predictions, total_predictions):
    # Calculate the percentage of correct and wrong predictions
    correct_percentage = round(correct_predictions / total_predictions, 3)
    wrong_percentage = round(wrong_predictions / total_predictions, 3)
    # Calculate the overall accuracy
    accuracy = round((correct_predictions * 100) / total_predictions, 3)
    return correct_percentage, wrong_percentage, accuracy

# Load face images dataset from a ZIP file
zipfile_path = "/Users/anveshmuppeda/Desktop/Anvesh/Courses/spring24/PR/project-pca/Dataset_images.zip"
face_images = load_face_images(zipfile_path)

# Split the data into training and testing sets
training_set, testing_set = split_data(zipfile_path)

# Function to perform recognition on a selected image
def recognize_selected_image(selected_filename):
    # Prepare the face image matrix for PCA
    image_matrix = []
    image_labels = []
    for key, val in training_set.items():
        image_matrix.append(val.flatten())  # Flatten each face image
        image_labels.append(key.split("/")[0])  # Extract the person label

    # Convert the face image matrix to a numpy array
    image_matrix = np.array(image_matrix)

    # Initialize and fit PCA to compute eigenfaces
    pca = PCA().fit(image_matrix)

    # Get the first n_components eigenfaces
    n_components = 10  # Choose the number of principal components
    eigenfaces = pca.components_[:n_components]

    # Compute the weights of face images with respect to the eigenfaces
    weights = eigenfaces @ (image_matrix - pca.mean_).T

    # Load the selected image
    selected_image = face_images[selected_filename].reshape(1, -1)

    # Compute the weights of the selected image with respect to the eigenfaces
    selected_image_weight = eigenfaces @ (selected_image - pca.mean_).T

    # Calculate Euclidean distance between the selected image and training images
    euclidean_distance = np.linalg.norm(weights - selected_image_weight, axis=0)

    # Find the best match
    best_match_index = np.argmin(euclidean_distance)
    best_match_label = image_labels[best_match_index]

    # Visualize the selected image and best match
    fig, axes = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(8, 6))
    axes[0].imshow(selected_image.reshape(val.shape), cmap="gray")
    axes[0].set_title("Selected Image")
    axes[1].imshow(image_matrix[best_match_index].reshape(val.shape), cmap="gray")
    axes[1].set_title("Best Match")
    plt.show()

    return best_match_label

# Example usage:
selected_filename = "Grp13Person22/211_22.jpg"  # Replace with the filename of the selected image
predicted_person = recognize_selected_image(selected_filename)
print("Predicted Person:", predicted_person)
