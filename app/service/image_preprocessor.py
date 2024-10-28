import cv2
import os
import numpy as np
import re
from app.service.prediction_service import get_predicted_mask_with_unpatchify
from app.service.index_analysis_service import calculate_ndvi_index_full_map, calculate_indices_and_stats_for_patches, calculate_ndvi, calculate_rendvi, calculate_cire, calculate_pri
from app import celery

from sklearn.preprocessing import MinMaxScaler
from patchify import patchify, unpatchify

from PIL import Image

minmaxscaler = MinMaxScaler()

image_patch_size = 256


def save_images_to_storage(image):
    output_path = 'outputs/output_image.png'
    # Normalize the array to the range 0-255
    image_array_normalized = (image * 255).astype(np.uint8)
    if image_array_normalized.ndim == 3 and image_array_normalized.shape[-1] == 1:
        image_array_normalized = np.squeeze(image_array_normalized, axis=-1)
    
    # Since this is a single-channel image, no need for cv2.cvtColor
    # Convert NumPy array directly to a Pillow Image in 'L' mode for grayscale
    pil_image = Image.fromarray(image_array_normalized, mode='L')
    
    # Save the image
    pil_image.save(output_path)
    print(f"Image saved to {output_path}")

def load_images_from_storage(image_paths):
    images = []

    for path in image_paths:
        try:
            # Check if the file exists at the given path
            if os.path.exists(path):
                # Read the image with cv2 using IMREAD_UNCHANGED to preserve the original format
                image_data = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                
                # Ensure the image was loaded successfully
                if image_data is not None:
                    # Get the file name from the path
                    file_name = os.path.basename(path)
                    
                    # Append both the image data and the file name as a tuple
                    images.append((image_data, file_name))
                else:
                    print(f"Failed to load image (Invalid format or corrupted): {path}")
            else:
                print(f"File not found: {path}")
        
        except Exception as e:
            print(f"Failed to load image: {path}, Error: {e}")
    
    print(f"Loaded {len(images)} image files successfully.")
    return images

def resize_images_to_smallest(images):
    # Determine the smallest height and width among all images
    smallest_height = min(image_data.shape[0] for image_data, _ in images)  # Height is the 1st dimension
    smallest_width = min(image_data.shape[1] for image_data, _ in images)   # Width is the 2nd dimension

    resized_images = []

    for image_data, file_name in images:
        # Resize image using cv2 to the smallest dimensions
        resized_data = cv2.resize(image_data, (smallest_width, smallest_height), interpolation=cv2.INTER_LINEAR)
        
        # Append the resized image and file name to the list
        resized_images.append((resized_data, file_name))

    print(f"Resized all images to {smallest_width}x{smallest_height}")
    return resized_images

def categorize_images_by_band(loaded_images):
    categorized_images = {
        'RGB': None,
        'Green': None,
        'NIR': None,
        'RED': None,
        'RE': None
    }

    # Patterns to identify each band type based on the file name
    band_patterns = {
        'RGB': re.compile(r'_D\.(jpg|jpeg|png)$', re.IGNORECASE),  # Matches '_D.JPG', '_D.PNG', etc.
        'Green': re.compile(r'_MS_G\.tif$', re.IGNORECASE),        # Matches '_MS_G.TIF'
        'NIR': re.compile(r'_MS_NIR\.tif$', re.IGNORECASE),        # Matches '_MS_NIR.TIF'
        'RED': re.compile(r'_MS_R\.tif$', re.IGNORECASE),          # Matches '_MS_R.TIF'
        'RE': re.compile(r'_MS_RE\.tif$', re.IGNORECASE)           # Matches '_MS_RE.TIF'
    }

    # Categorize each loaded image by matching filename patterns
    for image_data, file_name in loaded_images:
        for band, pattern in band_patterns.items():
            if pattern.search(file_name):
                categorized_images[band] = (image_data, file_name)  # Store the image and file name
                break

    return categorized_images

def align_images(base_image, band_image):
    print("Alignment Start")
    # Check if band image is in 16-bit, and if so, convert it to 8-bit
    if band_image.dtype == np.uint16:
        # Normalize the 16-bit image to 8-bit
        band_image = cv2.normalize(band_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Convert both images to grayscale for feature detection
    base_gray = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
    band_gray = band_image  # If the NIR image is already single-channel

    # Use SIFT to detect keypoints and descriptors
    sift = cv2.SIFT_create()

    keypoints1, descriptors1 = sift.detectAndCompute(base_gray, None)
    keypoints2, descriptors2 = sift.detectAndCompute(band_gray, None)

    # Use BFMatcher to match descriptors
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Apply ratio test as per Lowe's paper
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Extract location of good matches
    if len(good_matches) > 4:
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Compute homography matrix
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Warp the RGB image to align with the band image
        height, width = band_image.shape[:2]
        aligned_base = cv2.warpPerspective(base_image, H, (width, height))
        print("Alignment Successfull")
        return aligned_base, band_image
    else:
        print("Not enough good matches found!")
        return None, None

def patch_and_normalize_for_prediction( image, image_patch_size):
    normalized_patched_images = []

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
    return send_for_pred, patched_images
    
def remove_background(image, binary_mask):
    # Check if the input image is 3-channel or 1-channel
    if len(image.shape) == 3 and image.shape[2] == 3:  # RGB Image
        binary_mask = (binary_mask * 255).astype(np.uint8) 
        binary_mask_3channel = cv2.cvtColor(binary_mask, cv2.COLOR_GRAY2BGR)
        result_image = cv2.bitwise_and(image, binary_mask_3channel)
    elif len(image.shape) == 2 and image.dtype == 'uint16':  # 1-channel Image
        # Use the binary mask directly for 1-channel image
        binary_mask = (binary_mask * 65535).astype(np.uint16) 
        result_image = cv2.bitwise_and(image, binary_mask)
    elif len(image.shape) == 2 and image.dtype == 'uint8':  # 1-channel Image
        # Use the binary mask directly for 1-channel image
        binary_mask = (binary_mask * 255).astype(np.uint8) 
        result_image = cv2.bitwise_and(image, binary_mask)
    else:
        raise ValueError("Input image must be either a 1-channel or a 3-channel image.")
    
    return result_image

@celery.task(bind=True, rate_limit='2/m')
def preprocessor(self, image_urls):
    try:
        images = load_images_from_storage(image_urls)
        images = resize_images_to_smallest(images)
        categorized_images = categorize_images_by_band(images)

        rgb_image_nparray = np.array(categorized_images.get('RGB')[0])
        nir_image_nparray = np.array(categorized_images.get('NIR')[0])
        red_image_nparray = np.array(categorized_images.get('RED')[0])
        green_image_nparray = np.array(categorized_images.get('Green')[0])
        re_image_nparray = np.array(categorized_images.get('RE')[0])
        
        aligned_rgb, band_image = align_images(rgb_image_nparray, nir_image_nparray)

        input_img, patched_images = patch_and_normalize_for_prediction(aligned_rgb, image_patch_size)
    
        predicted_mask = get_predicted_mask_with_unpatchify(input_img, patched_images)
        resized_mask = cv2.resize(predicted_mask, (rgb_image_nparray.shape[1], rgb_image_nparray.shape[0]))

        result_rgb_mask = remove_background(rgb_image_nparray, resized_mask)

        result_image_red = remove_background(red_image_nparray, resized_mask)
        result_image_nir = remove_background(nir_image_nparray, resized_mask)
        result_image_green = remove_background(green_image_nparray, resized_mask)
        result_image_re= remove_background(re_image_nparray, resized_mask)

        ndvi = calculate_ndvi_index_full_map(result_image_red, result_image_nir)

        nir_band_patches = patchify(result_image_nir, (image_patch_size, image_patch_size), step=image_patch_size)
        red_band_patches = patchify(result_image_red, (image_patch_size, image_patch_size), step=image_patch_size)
        green_band_patches = patchify(result_image_green, (image_patch_size, image_patch_size), step=image_patch_size)
        re_band_patches = patchify(result_image_re, (image_patch_size, image_patch_size), step=image_patch_size)

        ndvi_patches, ndvi_stats = calculate_indices_and_stats_for_patches(nir_band_patches, red_band_patches, calculate_ndvi, 'ndvi')
        rendvi_patches, rendvi_stats = calculate_indices_and_stats_for_patches(nir_band_patches, re_band_patches, calculate_rendvi, 'rendvi')
        cire_patches, cire_stats = calculate_indices_and_stats_for_patches(nir_band_patches, red_band_patches, calculate_cire, 'cire')
        pri_patches, pri_stats = calculate_indices_and_stats_for_patches(green_band_patches, red_band_patches, calculate_pri, 'pri')
        
        # Combine all stats into one dictionary
        patches = []
        for ndvi_patch, rendvi_patch, cire_patch, pri_patch in zip(ndvi_stats, rendvi_stats, cire_stats, pri_stats):
                # Merge all index stats for the same patch
            combined_patch = {
                'ndvi': ndvi_patch['ndvi'],
                'rendvi': rendvi_patch['rendvi'],
                'cire': cire_patch['cire'],
                'pri': pri_patch['pri'],
                'row': ndvi_patch['row'],
                'column': ndvi_patch['column']
            }
            patches.append(combined_patch)
        return {"patches": patches}
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise e
    
