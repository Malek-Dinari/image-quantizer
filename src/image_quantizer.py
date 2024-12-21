import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class KMeansScratch:
    def __init__(self, n_clusters, max_iters=300, tol=1e-4):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None

    def fit(self, data):
        # Randomly initialize centroids
        np.random.seed(42)
        random_indices = np.random.choice(len(data), self.n_clusters, replace=False)
        self.centroids = data[random_indices]

        for iteration in range(self.max_iters):
            # Assign clusters based on closest centroid
            distances = self._compute_distances(data, self.centroids)
            labels = np.argmin(distances, axis=1)

            # Compute new centroids
            new_centroids = []
            for i in range(self.n_clusters):
                cluster_points = data[labels == i]
                if len(cluster_points) == 0:  # Handle empty clusters
                    new_centroids.append(data[np.random.choice(len(data))])
                else:
                    new_centroids.append(cluster_points.mean(axis=0))
            new_centroids = np.array(new_centroids)

            # Check for convergence
            if np.all(np.linalg.norm(new_centroids - self.centroids, axis=1) < self.tol):
                break

            self.centroids = new_centroids

        return labels

    def _compute_distances(self, data, centroids):
        return np.linalg.norm(data[:, None] - centroids, axis=2)

# Function to apply K-means quantization to an image
def quantize_image(image_path, output_path, n_colors=16):
    # Load and preprocess the image
    image = Image.open(image_path)
    image = np.array(image) / 255.0  # Normalize pixel values
    h, w, c = image.shape
    pixels = image.reshape(-1, c)

    # Apply K-means from scratch
    kmeans = KMeansScratch(n_clusters=n_colors)
    labels = kmeans.fit(pixels)

    # Reconstruct the quantized image
    quantized_pixels = kmeans.centroids[labels]
    quantized_image = quantized_pixels.reshape(h, w, c)

    # Save the quantized image
    quantized_image_pil = Image.fromarray((quantized_image * 255).astype(np.uint8))
    quantized_image_pil.save(output_path)

    # Display the original and quantized images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(image)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title(f"Quantized Image (K={n_colors})")
    plt.imshow(quantized_image)
    plt.axis("off")

    plt.show()

# Paths
input_path = r"C:\Users\Lenovo\Desktop\programming\TASKS-and-PROJECTS-2024-25\Personal-tomfoolery\ImageQuantizer\assets\HZD-6.png"
output_path = r"C:\Users\Lenovo\Desktop\programming\TASKS-and-PROJECTS-2024-25\Personal-tomfoolery\ImageQuantizer\outputs\quantized_HZD-6.png"

# Run the quantization process
quantize_image(input_path, output_path, n_colors=16)
