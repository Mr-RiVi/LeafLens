import cv2
import os
import numpy as np
import re
import rasterio
from rasterio.enums import Resampling

def resize_images_to_smallest(images):
    """
    Resize multispectral images to the smallest resolution among them using Rasterio.

    Args:
        images (list of tuples): A list containing tuples of (image_data, metadata).
                                 Each tuple represents (image_data, metadata) where 
                                 image_data is a numpy array of the image bands and 
                                 metadata is a dictionary of image metadata.

    Returns:
        list: A list of resized images with preserved metadata.
    """
    # Determine the smallest height and width among all images
    smallest_height = min(metadata['height'] for _, metadata in images)
    smallest_width = min(metadata['width'] for _, metadata in images)

    resized_images = []

    for image_data, metadata in images:
        # Calculate the new transform to maintain metadata consistency
        transform = metadata['transform']
        new_transform = transform * transform.scale(
            (metadata['width'] / smallest_width),
            (metadata['height'] / smallest_height)
        )
        
        # Update metadata with the new dimensions and transform
        new_metadata = metadata.copy()
        new_metadata.update({
            'height': smallest_height,
            'width': smallest_width,
            'transform': new_transform
        })

        # Resampling the image to the new size
        with rasterio.MemoryFile() as memfile:
            with memfile.open(**new_metadata) as dataset:
                resized_data = dataset.read(
                    out_shape=(dataset.count, smallest_height, smallest_width),
                    resampling=Resampling.bilinear  # Change to Resampling.nearest if no interpolation is desired
                )

                resized_images.append((resized_data, new_metadata))
    
    return resized_images

def save_resized_images(resized_images, output_dir='resized_output_images'):
    """
    Save resized multispectral images to a specified directory.

    Args:
        resized_images (list of tuples): A list containing tuples of (resized_image_data, metadata).
                                         Each tuple represents (resized_image_data, metadata) where 
                                         resized_image_data is a numpy array of the resized image bands and 
                                         metadata is a dictionary of image metadata.
        output_dir (str): The directory where resized images will be saved. Defaults to 'resized_output_images'.
    """
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through the list of resized images
    for idx, (image_data, metadata) in enumerate(resized_images):
        # Define the output file path
        output_path = os.path.join(output_dir, f'resized_image_{idx+1}.tif')

        # Save the resized image using rasterio
        try:
            with rasterio.open(
                output_path, 'w',
                driver=metadata['driver'],
                height=metadata['height'],
                width=metadata['width'],
                count=image_data.shape[0],  # Number of bands
                dtype=image_data.dtype,
                crs=metadata['crs'],  # Coordinate Reference System
                transform=metadata['transform']
            ) as dst:
                dst.write(image_data)  # Write the resized image data to the file

            print(f"Saved resized image to {output_path}")

        except Exception as e:
            print(f"Failed to save image {output_path}: {e}")

def load_images_from_storage(image_paths):
    """
    Load multispectral images from local paths and return them with their metadata.

    Args:
        image_paths (list): List of local paths pointing to the images.

    Returns:
        list: A list of tuples containing the image data and metadata for each image.
    """
    images = []
    
    for path in image_paths:
        try:
            # Check if the file exists at the given path
            if os.path.exists(path):
                # Open the image using Rasterio to preserve metadata
                with rasterio.open(path) as src:
                    image_data = src.read()  # Read all bands
                    metadata = src.meta
                    images.append((image_data, metadata))
            else:
                print(f"File not found: {path}")
        
        except Exception as e:
            print(f"Failed to load image: {path}, Error: {e}")
    
    print(f"Loaded {len(images)} image files successfully.")
    return images

def categorize_images_by_band(images_dir_path):
    # List all image files in the input directory
    image_files = [f for f in os.listdir(images_dir_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff'))]

    pattern = re.compile(r'_(\d{4})_')  # Pattern to identify the unique set identifier
    image_sets = {}
    input_dir = 'output_dir'
    for filename in os.listdir(input_dir):
        match = pattern.search(filename)
        if match:
            set_id = match.group(1)
            if set_id not in image_sets:
                image_sets[set_id] = {}
            
            if "MS_R" in filename:
                image_sets[set_id]['red'] = os.path.join(input_dir, filename)
            elif "MS_NIR" in filename:
                image_sets[set_id]['nir'] = os.path.join(input_dir, filename)
            elif "MS_G" in filename:
                image_sets[set_id]['green'] = os.path.join(input_dir, filename)
            elif "MS_RE" in filename:
                image_sets[set_id]['red_edge'] = os.path.join(input_dir, filename)
            elif "D" in filename:
                image_sets[set_id]['rgb'] = os.path.join(input_dir, filename)

    print("image sets: ",image_sets)
    return

def preprocessor(image_urls):
    """
    Image Preprocessor.
    
    Args:
        image_urls (list): List of URLs pointing to the images to be processed.
    
    Returns:
        list: A list of processed images and their metadata.
    """

    images = load_images_from_storage(image_urls)

    # Resize images to the smallest common resolution
    resized_images = resize_images_to_smallest(images)
    save_resized_images(images)
    return
    
    # Save resized images to the output directory
    # save_resized_images(resized_images, image_files, 'output_dir')
    return resized_images