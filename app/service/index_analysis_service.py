import rasterio
import numpy as np
import re
import os

# TODO: NDVI, RENDVI, CIRE, PRI

# RENDVI - The value of this index ranges from -1 to 1. The common range for green vegetation is 0.2 to 0.9.
# PRI - The values range from –1 to 1.

def save_ndvi(ndvi, reference_band_path, output_path):
    """
    Save NDVI results to a GeoTIFF file using metadata from a reference band.
    
    Args:
        ndvi (np.ndarray): NDVI values to save.
        reference_band_path (str): Path to a band image to use for georeferencing.
        output_path (str): Path to save the NDVI image.
    """
    with rasterio.open(reference_band_path) as ref_src:
        meta = ref_src.meta
        meta.update(driver='GTiff', dtype=rasterio.float32, count=1)
        
        with rasterio.open(output_path, 'w', **meta) as dst:
            dst.write(ndvi.astype(rasterio.float32), 1)

def calculate_rendvi(band_red_edge, band_nir):
    red_edge = band_red_edge[0].astype('float64')
    nir = band_nir[0].astype('float64')

    # Calculate RENDVI
    rendvi = np.where(
        (nir + red_edge) == 0., 
        0, 
        (nir - red_edge) / (nir + red_edge)
    )

    return {
        'mean': np.mean(rendvi),
        'median': np.median(rendvi),
        'min': np.min(rendvi),
        'max': np.max(rendvi),
        'std_dev': np.std(rendvi)
    }

def calculate_cire(band_nir, band_re):
    """
    Calculate the Chlorophyll Index Red Edge (CIRE).

    Parameters:
    - band_nir: Tuple (image_array, metadata) for the Near-Infrared band
    - band_re: Tuple (image_array, metadata) for the Red Edge band

    Returns:
    - Dictionary containing:
      - 'cire_array': The calculated CIRE array
      - 'mean': Mean value of CIRE
      - 'median': Median value of CIRE
      - 'min': Minimum value of CIRE
      - 'max': Maximum value of CIRE
      - 'std_dev': Standard deviation of CIRE
    """
    # Access the image arrays from the tuples
    nir_array = band_nir[0]  # First element is the image data
    re_array = band_re[0]    # First element is the image data

    # Convert the arrays to float64 for precise calculations
    nir = nir_array.astype('float64')
    re = re_array.astype('float64')

    # Calculate CIRE
    cire = (nir / re) - 1

    # Return CIRE statistics and the CIRE array
    return {
        'mean': np.mean(cire),
        'median': np.median(cire),
        'min': np.min(cire),
        'max': np.max(cire),
        'std_dev': np.std(cire)
    }

def calculate_pri(band_green, band_red_edge):
    """
    Calculate the Photochemical Reflectance Index (PRI) using available bands.

    Parameters:
    - band_green: Tuple (image_array, metadata) for the Green band
    - band_red_edge: Tuple (image_array, metadata) for the Red Edge band

    Returns:
    - Dictionary containing:
      - 'pri_array': The calculated PRI array
      - 'mean': Mean value of PRI
      - 'median': Median value of PRI
      - 'min': Minimum value of PRI
      - 'max': Maximum value of PRI
      - 'std_dev': Standard deviation of PRI
    """
    # Access the image arrays from the tuples
    green_array = band_green[0]  # First element is the image data
    red_edge_array = band_red_edge[0]  # First element is the image data

    # Convert the arrays to float64 for precise calculations
    green = green_array.astype('float64')
    red_edge = red_edge_array.astype('float64')

    # Calculate PRI
    pri = np.where(
        (green + red_edge) == 0., 
        0, 
        (green - red_edge) / (green + red_edge)
    )

    # Return PRI statistics and the PRI array
    return {
        'mean': np.mean(pri),
        'median': np.median(pri),
        'min': np.min(pri),
        'max': np.max(pri),
        'std_dev': np.std(pri)
    }

def calculate_ndvi(band_red, band_nir):
    red = band_red[0].astype('float64')
    nir = band_nir[0].astype('float64') 

    #ndvi calculation, empty cells or nodata cells are reported as 0
    ndvi=np.where(
        (nir+red)==0., 
        0, 
        (nir-red)/(nir+red))
    ndvi[:5,:5]

    mean_ndvi = np.mean(ndvi)
    median_ndvi = np.median(ndvi)
    min_ndvi = np.min(ndvi)
    max_ndvi = np.max(ndvi)
    std_dev_ndvi = np.std(ndvi)

    ndvi_results = {
        'mean': mean_ndvi,
        'median': median_ndvi,
        'min': min_ndvi,
        'max': max_ndvi,
        'std_dev': std_dev_ndvi
    }
    
    return ndvi_results

def calculate_indexes(image_set):

    ndvi_results = calculate_ndvi(image_set.get('RED'), image_set.get('NIR'))
    rendvi_results = calculate_rendvi(image_set.get('RE'), image_set.get('NIR'))
    cire_results = calculate_cire(image_set.get('NIR'), image_set.get('RE'))
    pri_results = calculate_pri(image_set.get('Green'), image_set.get('RE'))

    return ndvi_results, rendvi_results, cire_results, pri_results

def calculate_ndvi_index_full_map(result_image_red, result_image_nir):
    result_image_red = result_image_red.astype(np.float64)
    result_image_nir = result_image_nir.astype(np.float64)

    #ndvi calculation, empty cells or nodata cells are reported as 0
    ndvi=np.where(
        (result_image_nir+result_image_red)==0., 
        0, 
        (result_image_nir-result_image_red)/(result_image_nir+result_image_red))
    ndvi[:5,:5]

    return ndvi

def calculate_ndvi(result_image_nir, result_image_red):
    ndvi=np.where(
        (result_image_nir+result_image_red)==0., 
        0, 
        (result_image_nir-result_image_red)/(result_image_nir+result_image_red))
    ndvi[:5,:5]

    return ndvi

# Function to calculate RENDVI
def calculate_rendvi(nir_patch, red_edge_patch):
    return np.where((nir_patch + red_edge_patch) == 0., 0, (nir_patch - red_edge_patch) / (nir_patch + red_edge_patch))

# Function to calculate CIRE
def calculate_cire(nir_patch, red_patch):
    return np.where(red_patch == 0., 0, nir_patch / red_patch - 1)

# Function to calculate PRI
def calculate_pri(green_patch, red_patch):
    return np.where((green_patch + red_patch) == 0., 0, (green_patch - red_patch) / (green_patch + red_patch))

def calculate_indices_and_stats_for_patches(band1_patches, band2_patches, index_calculation_func, index_name):
    patches = []
    patch_list = []

    # Loop through patches and calculate the index
    for i in range(band1_patches.shape[0]):
        row_patches = []
        for j in range(band1_patches.shape[1]):
            # Get the corresponding band patches
            band1_patch = band1_patches[i, j, :, :].astype(np.float64)
            band2_patch = band2_patches[i, j, :, :].astype(np.float64)

            # Apply the index calculation function
            index_patch = index_calculation_func(band1_patch, band2_patch)
            row_patches.append(index_patch)

            # Compute statistics for the patch
            mean_index = np.mean(index_patch)
            median_index = np.median(index_patch)
            min_index = np.min(index_patch)
            max_index = np.max(index_patch)
            std_dev_index = np.std(index_patch)

            # Add the stats to the list for this patch
            patch_stats = {
                index_name: {
                    'mean': mean_index,
                    'median': median_index,
                    'min': min_index,
                    'max': max_index,
                    'std_dev': std_dev_index
                },
                'row': i,
                'column': j
            }

            # Append the patch stats to the list
            patch_list.append(patch_stats)
        
        patches.append(row_patches)
    patches = np.array(patches)
    return patches, patch_list