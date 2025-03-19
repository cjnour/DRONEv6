import os
import itertools
import cv2
import numpy as np

# This script will show you how a label with polygonal formatting
# displays the bounding box on its corresponding image.

# Path to your image
IMAGE_PATH = "C:/Users/Charb/Desktop/asd.jpg"  # Change this to your actual image path

# Label values (without the class ID)
label_values = [0.8, 0.023437500000000066, 0.2734375, 0.023437500000000035, 
                0.27343750000000006, 0.6125, 0.8, 0.6125000000000002]

# Load image
image = cv2.imread(IMAGE_PATH)
if image is None:
    raise FileNotFoundError(f"Could not load image at {IMAGE_PATH}")

height, width, _ = image.shape  # Get image dimensions

# Convert normalized coordinates to pixel values
points = [(int(label_values[i] * width), int(label_values[i+1] * height)) for i in range(0, len(label_values), 2)]

# Draw each point on the image
for i, (x, y) in enumerate(points):
    cv2.circle(image, (x, y), radius=5, color=(0, 0, 255), thickness=-1)
    cv2.putText(image, f"P{i+1}", (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Save output image
cv2.imwrite("output_points.jpg", image)

print("Plotted points saved as 'output_points.jpg'. Check and analyze their positions.")