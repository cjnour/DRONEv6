import os

# This script will convert YOLOv8 labels (that use polygon mask points) to
# a 5-parameter label, suitable for most YOLO models.

# Paths (update if needed)
LABELS_DIR = "C:/Users/Charb/Desktop/droneDataset/labels/valid"  # Folder containing corresponding images
OUTPUT_DIR = "C:/Users/Charb/Desktop/droneDataset/converted_valid_labels"  # Save convert

os.makedirs(OUTPUT_DIR, exist_ok=True)  # Create output folder if needed

def convert_polygon_to_bbox(label_file):
    """ Convert YOLOv8 polygon labels into YOLOv6 bounding box format. """

    # Read label file
    with open(label_file, "r") as file:
        lines = file.readlines()

    new_lines = []
    
    for line in lines:
        parts = line.strip().split()
        if len(parts) > 5:  # If extra parameters exist (YOLOv8-style)
            class_id = parts[0]
            points = [float(p) for p in parts[1:]]  # Convert to float

            # Extract bounding box from the first four points
            x_values = points[0::2]  # X-coordinates
            y_values = points[1::2]  # Y-coordinates

            x_min, x_max = min(x_values), max(x_values)
            y_min, y_max = min(y_values), max(y_values)

            # Convert to YOLOv6 format (already normalized!)
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            bbox_width = x_max - x_min
            bbox_height = y_max - y_min

            new_label = f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"
            new_lines.append(new_label)
        else:
            new_lines.append(line.strip())  # Keep original if already correct

    # Save converted label in OUTPUT_DIR
    output_label_path = os.path.join(OUTPUT_DIR, os.path.basename(label_file))
    with open(output_label_path, "w") as file:
        file.write("\n".join(new_lines) + "\n")

    return True

# Process all label files
label_files = [f for f in os.listdir(LABELS_DIR) if f.endswith(".txt")]
total_files = len(label_files)
processed_count = 0

for filename in label_files:
    label_path = os.path.join(LABELS_DIR, filename)

    if convert_polygon_to_bbox(label_path):
        processed_count += 1
        print(f"Processed [{processed_count}/{total_files}]: {filename}")

print(f"\n✅ All labels converted! Saved in '{OUTPUT_DIR}'.")
