import os
import shutil
import numpy as np
from PIL import Image
from pathlib import Path
from sklearn.cluster import KMeans



# Step 2: Load and preprocess the images
def preprocess_images(img_directory):
    image_paths = [os.path.join(img_directory, file) for file in os.listdir(img_directory)]
    images = []
    for path in image_paths:
        image = Image.open(path)
        image = image.resize((64, 64))  # Resize the image to a consistent size
        image_array = np.array(image).flatten()  # Flatten the image into a 1D array
        images.append(image_array)
    return images


def convert_images_to_array(images):
    images_array = np.array(images)
    return images_array


# Step 4: Apply K-means clustering
def cluster_images(images_array, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(images_array)
    return kmeans

def get_img_clusters_with_label(kmeans, image_paths):
    labels = kmeans.labels_
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(image_paths[i])
    return clusters


def save_images_to_cluster(clusters):
    for label, cluster_images in clusters.items():
        print(f"Cluster {label+1}:")
        Path(f'./data/{label}').mkdir(parents=True, exist_ok=True)
        for img_walker, image_path in enumerate(cluster_images):
            source_file = image_path # Replace with the path to the source file
            destination_file = f"./data/{label}/{img_walker}.jpg"  # Replace with the path to the destination file

            # Copy the file
            shutil.copyfile(source_file, destination_file)


if __name__ == "__main__":
    img_directory = "./data/sample_images"
    images = preprocess_images(img_directory)
    images_array = convert_images_to_array(images)
    num_clusters = 5  # Adjust the number of clusters as per your needs
    kmeans = cluster_images(images_array, num_clusters)
    image_paths = [os.path.join(img_directory, file) for file in os.listdir(img_directory)]
    clusters = get_img_clusters_with_label(kmeans, image_paths)
    save_images_to_cluster(clusters)