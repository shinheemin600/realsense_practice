from PIL import Image
import numpy as np
import os

# --- Configuration ---
# This is the file you uploaded
input_jpg_file = '111111_Depth.png'

# These are the files we will create
output_png_file = 'output_image1.png'
output_raw_file = 'output_data1.raw'
output_csv_file = 'output_data1.csv' # Added CSV output file

# Check if the input file exists
if not os.path.exists(input_jpg_file):
print(f"Error: Input file '{input_jpg_file}' not found.")
print("Please make sure the file is in the same directory as the script.")
else:
# --- 1. Load the Image ---
print(f"Loading image: {input_jpg_file}...")
with Image.open(input_jpg_file) as img:
    # Get image details (for our reference)
    width, height = img.size
    mode = img.mode
    print(f"Image loaded successfully ({width}x{height}, Mode: {mode})")

    # --- 2. Make the PNG file ---
    # This is straightforward. Pillow handles the conversion.
    try:
        img.save(output_png_file)
        print(f"Successfully created PNG file: {output_png_file}")
    except Exception as e:
        print(f"Error creating PNG file: {e}")

    # --- 3. Make the RAW data file ---
    # Convert the image to a NumPy array to get the raw pixel data
    # For an RGB image, this will be an array of shape (height, width, 3)
    # with uint8 (0-255) values for Red, Green, and Blue.
    raw_pixel_data = np.array(img)
    
    # Save this array to a file as raw binary data
    try:
        # .tofile() writes the array's data as-is, with no header
        raw_pixel_data.tofile(output_raw_file)
        print(f"Successfully created RAW data file: {output_raw_file}")
        
        print("\n--- To read this .raw file later (e.g., in numpy) ---")
        print("You must know its properties:")
        print(f" - Shape (height, width, channels): ({height}, {width}, {len(mode)})")
        print(f" - Data type: {raw_pixel_data.dtype}")
        print(f"Example read command:")
        print(f"shape = ({height}, {width}, {len(mode)})")
        print(f"dtype = np.{raw_pixel_data.dtype}")
        print(f"read_data = np.fromfile('{output_raw_file}', dtype=dtype).reshape(shape)")

    except Exception as e:
        print(f"Error creating RAW file: {e}")

    # --- 4. Make the CSV file from RAW data ---
    print(f"\nCreating CSV file: {output_csv_file}...")
    
    try:
        # We already have the raw_pixel_data as a numpy array
        # Its shape is (height, width, channels)
        
        # Open the CSV file for writing
        with open(output_csv_file, 'w') as f:
            # Write the header based on the image mode (e.g., RGB, L)
            if mode == 'RGB':
                f.write('row,column,R,G,B\n')
            elif mode == 'L': # Grayscale
                f.write('row,column,Value\n')
            else: # Handle other modes like RGBA
                header_channels = ','.join(list(mode))
                f.write(f'row,column,{header_channels}\n')
            
            # Iterate over each pixel and write its row, column, and value(s)
            for r in range(height):
                for c in range(width):
                    pixel_value = raw_pixel_data[r, c]
                    
                    # Format the pixel value for the CSV
                    if isinstance(pixel_value, np.ndarray):
                        # For RGB/RGBA, pixel_value is an array [R, G, B]
                        value_str = ','.join(map(str, pixel_value))
                    else:
                        # For 'L' (grayscale), pixel_value is a single number
                        value_str = str(pixel_value)
                        
                    f.write(f'{r},{c},{value_str}\n')
        
        print(f"Successfully created CSV file: {output_csv_file}")

    except Exception as e:
        print(f"Error creating CSV file: {e}")


