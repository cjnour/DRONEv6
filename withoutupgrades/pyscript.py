import os

# Define dataset paths (update these if needed)
dataset_dirs = ["labels/test", "labels/train", "labels/valid"]

def convert_yolo_labels(label_dir):
    file_count = 1

    # Loop through all label files
    for filename in os.listdir(label_dir):
        file_path = os.path.join(label_dir, filename)

        # Ensure it's a .txt file
        if filename.endswith(".txt"):
            with open(file_path, "r") as file:
                lines = file.readlines()

            # Process each line in the file
            new_lines = []
            for line in lines:
                parts = line.strip().split()  # Split line into parts
                if len(parts) > 5:  # Check if it's a YOLOv8 label
                    new_line = " ".join(parts[:5])  # Keep only first 5 values
                    new_lines.append(new_line)
                else:
                    new_lines.append(line.strip())  # Keep as is

            # Overwrite the file with the corrected labels
            with open(file_path, "w") as file:
                file.write("\n".join(new_lines) + "\n")

            print(f"Processed [{file_count}]: {file_path}")
            file_count += 1  # Increment the counter

# Run conversion on both "train" and "test" label folders
for label_folder in dataset_dirs:
    if os.path.exists(label_folder):
        convert_yolo_labels(label_folder)
    else:
        print(f"Warning: {label_folder} does not exist.")

print("Conversion complete!")
