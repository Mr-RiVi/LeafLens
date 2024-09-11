import cv2
import os
import numpy as np
import re
import rasterio
from rasterio.enums import Resampling
from app.service.prediction_service import get_predicted_mask

from sklearn.preprocessing import MinMaxScaler
from patchify import patchify

from PIL import Image

minmaxscaler = MinMaxScaler()

def resize_images_to_smallest(images):
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
                    resampling=Resampling.bilinear
                )

                resized_images.append((resized_data, new_metadata))
    
    return resized_images

def save_resized_images(resized_images, output_dir='resized_output_images'):
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
                count=image_data.shape[0],
                dtype=image_data.dtype,
                crs=metadata['crs'],
                transform=metadata['transform']
            ) as dst:
                dst.write(image_data)

            print(f"Saved resized image to {output_path}")

        except Exception as e:
            print(f"Failed to save image {output_path}: {e}")

####################################################################################################

def load_images_from_storage(image_paths):
    images = []
    
    for path in image_paths:
        try:
            # Check if the file exists at the given path
            if os.path.exists(path):
                # Open the image using Rasterio to preserve metadata
                with rasterio.open(path) as src:
                    image_data = src.read()
                    metadata = src.meta
                    images.append((image_data, metadata, path))
            else:
                print(f"File not found: {path}")
        
        except Exception as e:
            print(f"Failed to load image: {path}, Error: {e}")
    
    print(f"Loaded {len(images)} image files successfully.")
    return images

def categorize_images_by_band(loaded_images):
    categorized_images = {
        'RGB': None,
        'Green': None,
        'NIR': None,
        'RED': None,
        'RE': None
    }

    # Patterns to identify each band type
    band_patterns = {
        'RGB': re.compile(r'_D\.(jpg|jpeg|png)$', re.IGNORECASE),  # Matches '_D.JPG' etc.
        'Green': re.compile(r'_MS_G\.tif$', re.IGNORECASE),        # Matches '_MS_G.TIF'
        'NIR': re.compile(r'_MS_NIR\.tif$', re.IGNORECASE),       # Matches '_MS_NIR.TIF'
        'RED': re.compile(r'_MS_R\.tif$', re.IGNORECASE),         # Matches '_MS_R.TIF'
        'RE': re.compile(r'_MS_RE\.tif$', re.IGNORECASE)          # Matches '_MS_RE.TIF'
    }

    # Categorize each loaded image by matching filename patterns
    for image_data, metadata, path in loaded_images:
        filename = os.path.basename(path)
        for band, pattern in band_patterns.items():
            if pattern.search(filename):
                categorized_images[band] = (image_data, metadata)
                break

    return categorized_images

def norm_patch(image, image_patch_size = 256):
    
    normalized_patched_images = []

    image = np.array(image)
    image = np.transpose(image, (1, 2, 0))

    patched_images = patchify(image, (image_patch_size, image_patch_size, 3), step=image_patch_size)

    for i in range(patched_images.shape[0]):
        for j in range(patched_images.shape[1]):
            individual_patched_image = patched_images[i, j, :, :]
            individual_patched_image = minmaxscaler.fit_transform(
                            individual_patched_image.reshape(-1, individual_patched_image.shape[-1])
                        ).reshape(individual_patched_image.shape)
            normalized_patched_images.append(individual_patched_image)

    normalized_patched_images = np.array(normalized_patched_images)
    normalized_patched_images = np.squeeze(normalized_patched_images)
    send_for_pred = normalized_patched_images
    return send_for_pred

def reconstruct_mask2map(patches, image_height, image_width):
    # Extract patch dimensions
    patch_height, patch_width = patches.shape[1], patches.shape[2]

    # Calculate the number of patches along the height and width
    patches_per_row = image_width // patch_width
    patches_per_col = image_height // patch_height

    # Initialize an empty array for the full image
    full_image = np.zeros((image_height, image_width), dtype=patches.dtype)

    # Iterate over the patches and place them in the correct position
    patch_idx = 0
    for i in range(patches_per_col):
        for j in range(patches_per_row):
            # Calculate the position where this patch should be placed
            start_row = i * patch_height
            start_col = j * patch_width

            # Place the patch in the correct position
            full_image[start_row:start_row + patch_height, start_col:start_col + patch_width] = patches[patch_idx]
            patch_idx += 1

    return full_image

def preprocessor(image_urls):
    images = load_images_from_storage(image_urls)

    categorized_images = categorize_images_by_band(images)
    # print(categorized_images.get('RED')[0].shape)
    for_normalization = np.array(categorized_images.get('RGB')[0])

    rgb_image_height = categorized_images.get('RGB')[0].shape[1]
    rgb_image_width =categorized_images.get('RGB')[0].shape[2]

    for_prediction = norm_patch(for_normalization)

    predicted_mask = get_predicted_mask(for_prediction)

    reconstructed_mask = reconstruct_mask2map(predicted_mask, rgb_image_height, rgb_image_width)
    # print("hello",type(reconstructed_mask))
    # # Normalize the array to the range 0-255
    # image_array_normalized = (reconstructed_mask * 255).astype(np.uint8)

    # # Convert NumPy array to a Pillow Image
    # image = Image.fromarray(image_array_normalized)

    # # Save the image to a file
    # image.save('output_image.png')

    preprocessed_images = categorized_images

    return preprocessed_images