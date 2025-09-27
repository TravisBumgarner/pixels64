# Image Display System

This system converts square images into 8x8 color grids for display on your LED matrix.

## Setup

1. **Install Pillow** (for image processing):
   ```bash
   pip install Pillow
   ```

## Usage

### 1. Process Images

1. Place your square images in the `input/` directory
2. Supported formats: JPG, JPEG, PNG, BMP, GIF, TIFF
3. Run the processing script:
   ```bash
   cd src/images
   python3 process_images.py
   ```

This will:

- Resize each image to 8x8 pixels
- Extract RGB color data
- Generate `.py` files in the `output/` directory
- Create an `image_index.py` file listing all processed images

### 2. Display Images

The `display_images.py` file contains a `display_images()` function that:

- Automatically finds all processed images
- Cycles through them every 10 seconds
- Displays each image on your LED matrix

### 3. Integration

To use in your main display system, add this to your `main.py`:

```python
from images.display_images import display_images

displays_to_run = {
    "display_images": display_images,
    # ... other displays
}
```

## File Structure

```
images/
├── input/           # Put your source images here
├── output/          # Generated color data files
│   ├── __init__.py
│   ├── image_index.py  # Auto-generated list of images
│   └── *.py         # Individual image data files
├── process_images.py   # Image processing script
├── display_images.py   # Display function for MicroPython
└── README.md        # This file
```

## Image Processing Details

- Images are resized to 8x8 using high-quality LANCZOS resampling
- RGB values are extracted for each pixel
- Non-square images will be stretched to fit
- Color data is stored as tuples: `(r, g, b)` where each value is 0-255
