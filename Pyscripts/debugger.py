import os
import random
import cv2

# Paths (update if needed)
IMAGES_DIR = "C:/Users/Charb/Desktop/DRONEv6/images/valid"  # Folder containing images
LABELS_DIR = "C:/Users/Charb/Desktop/DRONEv6/labels/valid"  # Folder containing corresponding YOLOv6 labels
OUTPUT_DIR = "C:/Users/Charb/Desktop/output_debug"  # Folder to save debug images

os.makedirs(OUTPUT_DIR, exist_ok=True)  # Create folder if it doesn't exist

def draw_bboxes(image_path, label_path, output_path):
    """ Reads an image and its YOLO label, draws bounding boxes, and saves it. """
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Warning: Could not load {image_path}, skipping...")
        return

    height, width, _ = image.shape  # Image dimensions

    # Read label file
    if not os.path.exists(label_path):
        print(f"Warning: No label found for {image_path}, skipping...")
        return
    
    with open(label_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            print(f"Warning: Incorrect label format in {label_path}, skipping...")
            continue

        class_id, x_center, y_center, bbox_width, bbox_height = map(float, parts)

        # Convert YOLO format (normalized) to pixel values
        x_center, y_center = int(x_center * width), int(y_center * height)
        bbox_width, bbox_height = int(bbox_width * width), int(bbox_height * height)

        x1 = int(x_center - bbox_width / 2)
        y1 = int(y_center - bbox_height / 2)
        x2 = int(x_center + bbox_width / 2)
        y2 = int(y_center + bbox_height / 2)

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"Class {int(class_id)}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save output image
    cv2.imwrite(output_path, image)

# Select 20 random images
image_files = [f for f in os.listdir(IMAGES_DIR) if f.endswith(('.jpg', '.png'))]
random_images = random.sample(image_files, min(20, len(image_files)))  # Get up to 20 images

# Process selected images
for i, image_file in enumerate(random_images):
    image_path = os.path.join(IMAGES_DIR, image_file)
    label_path = os.path.join(LABELS_DIR, image_file.replace(".jpg", ".txt").replace(".png", ".txt"))
    output_path = os.path.join(OUTPUT_DIR, f"debug_{i+1}.jpg")

    draw_bboxes(image_path, label_path, output_path)
    print(f"Processed [{i+1}/20]: {image_file}")

print("\n✅ Debug images saved in 'output_debug/'. Check for bounding box accuracy!")
