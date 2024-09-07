import rasterio
import numpy as np
import re
import os

# TODO: NDVI, RENDVI, CIRE, PRI

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

def calculate_ndvi(red_band_path, nir_band_path):
    """
    Calculate NDVI using the formula (NIR - Red) / (NIR + Red).
    
    Args:
        red_band_path (str): Path to the Red band image.
        nir_band_path (str): Path to the NIR band image.
    
    Returns:
        np.ndarray: NDVI values as a numpy array.
    """
    with rasterio.open(red_band_path) as red_src:
        red_band = red_src.read(1)
    
    with rasterio.open(nir_band_path) as nir_src:
        nir_band = nir_src.read(1)
    
    np.seterr(divide='ignore', invalid='ignore')  # Ignore division by zero errors
    ndvi = (nir_band.astype(float) - red_band.astype(float)) / (nir_band + red_band)
    
    return ndvi

def calculate_indexes(image_sets):
    ndvi_results = {}

    for set_id, bands in image_sets.items():
        if 'red' in bands and 'nir' in bands:
            ndvi = calculate_ndvi(bands['red'], bands['nir'])
            ndvi_results[set_id] = ndvi
            
            # Save NDVI to a file
            output_path = f"ndvi_{set_id}.tif"
            save_ndvi(ndvi, bands['red'], output_path)
            print(f"NDVI for set {set_id} saved to {output_path}")
        else:
            print(f"Skipping set {set_id} - Missing necessary bands (Red, NIR).")

    return ndvi_results

    calculate_ndvi(preprocessed_images)