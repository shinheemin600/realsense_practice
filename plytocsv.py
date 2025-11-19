import numpy as np

# --- 1. EDIT THESE SETTINGS ---

# Path to your input .raw file
raw_file_path = '111111_Depth.raw'

# Path to your desired output .csv file
csv_file_path = '111111_Depth1.csv'

# Image dimensions (you MUST know these)
img_width = 424
img_height = 240

# Data type of the pixels in the raw file.
# Common depth formats:
# 'np.uint16' (for 16-bit unsigned integer)
# 'np.float32' (for 32-bit float)
# 'np.uint8'  (for 8-bit)
data_type = np.uint16

# --- 2. SCRIPT (No edits needed below) ---

print(f"Loading raw file: {raw_file_path}")

# Load the raw binary data from the file
# This reads the file as a 1D stream of data
try:
    depth_array_1d = np.fromfile(raw_file_path, dtype=data_type)
except FileNotFoundError:
    print(f"ERROR: File not found at {raw_file_path}")
    exit()

# Check if the loaded data matches the expected dimensions
expected_pixels = img_width * img_height
if depth_array_1d.size != expected_pixels:
    print(f"ERROR: File size does not match dimensions!")
    print(f"  File has {depth_array_1d.size} pixels.")
    print(f"  Expected {expected_pixels} (from {img_width}x{img_height}).")
    print("Please check your width, height, and data_type settings.")
    exit()

# Reshape the 1D array into a 2D array (image)
depth_image = depth_array_1d.reshape(img_height, img_width)

print(f"Reshaped to {depth_image.shape}")

# Save the 2D array to a CSV file
# 'delimiter=','' makes it a Comma Separated Value file
# 'fmt='%d'' formats the numbers as integers. Use '%.2f' for floats.
print(f"Saving to CSV: {csv_file_path}")
np.savetxt(csv_file_path, depth_image, delimiter=',', fmt='%d')

print("Conversion complete!")
