#!/usr/bin/env python3
"""
Image processing script to convert square images to 8x8 color grids.
Reads images from input/ directory and outputs Python code to copy into display_images.py
"""

import os
from PIL import Image


def process_image(image_path):
    """Process a single image into an 8x8 color grid."""
    try:
        # Open and convert image to RGB
        img = Image.open(image_path).convert("RGB")

        # Resize to 8x8 using LANCZOS resampling for better quality
        img_resized = img.resize((8, 8), Image.Resampling.LANCZOS)

        # Extract color data
        color_grid = []
        for y in range(8):
            row = []
            for x in range(8):
                r, g, b = img_resized.getpixel((x, y))
                row.append((r, g, b))
            color_grid.append(row)

        return color_grid

    except Exception as e:
        print(f"✗ Error processing {image_path}: {e}")
        return None


def main():
    """Process all images in the input directory and create Python code."""
    input_dir = "input"

    # Create input directory if it doesn't exist
    os.makedirs(input_dir, exist_ok=True)

    # Supported image formats
    supported_formats = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}

    # Find all image files in input directory
    image_files = []
    if os.path.exists(input_dir):
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                if ext in supported_formats:
                    image_files.append((file_path, filename))

    if not image_files:
        print(f"No supported image files found in {input_dir}/")
        print(f"Supported formats: {', '.join(supported_formats)}")
        return

    print(f"Found {len(image_files)} image(s) to process:")

    # Process each image and collect data
    images_data = []

    for file_path, filename in image_files:
        base_name = os.path.splitext(filename)[0]
        # Sanitize name for Python variable
        var_name = "".join(
            c if c.isalnum() or c == "_" else "_" for c in base_name
        ).upper()

        color_grid = process_image(file_path)
        if color_grid:
            images_data.append((var_name, base_name, color_grid))
            print(f"✓ Processed {filename}")

    if not images_data:
        print("No images were successfully processed!")
        return

    # Generate Python code
    output_file = "generated_images.txt"
    with open(output_file, "w") as f:
        f.write("# Generated image data - Copy this into display_images.py\n")
        f.write("# Replace the existing IMAGES dictionary with this code:\n\n")

        # Write individual image data
        for var_name, original_name, color_grid in images_data:
            f.write(f"# From {original_name}\n")
            f.write(f"{var_name} = [\n")
            for row in color_grid:
                f.write("    [")
                for i, color in enumerate(row):
                    if i > 0:
                        f.write(", ")
                    f.write(f"({color[0]}, {color[1]}, {color[2]})")
                f.write("],\n")
            f.write("]\n\n")

        # Write the IMAGES dictionary
        f.write("IMAGES = {\n")
        for var_name, original_name, _ in images_data:
            f.write(f'    "{original_name}": {var_name},\n')
        f.write("}\n")

    print(f"\n✓ Generated Python code in {output_file}")
    print("Copy the contents of this file into your display_images.py")


if __name__ == "__main__":
    main()
