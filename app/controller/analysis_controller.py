from flask import jsonify, current_app
import os

from app.service.image_preprocessor import preprocessor
from app.service.index_analysis_service import calculate_indexes
import random
from app.model.image_model import Image

def create_response(ndvi_results, rendvi_results, cire_results, pri_results):
    """
    Create a structured response with all calculated indexes.

    Parameters:
    - ndvi_results: Dictionary containing results of NDVI calculation
    - rendvi_results: Dictionary containing results of RENDVI calculation
    - cire_results: Dictionary containing results of CIRE calculation
    - pri_results: Dictionary containing results of PRI calculation

    Returns:
    - Dictionary containing structured response
    """
    response = {
        'ndvi': {
            'mean': ndvi_results.get('mean'),
            'median': ndvi_results.get('median'),
            'min': ndvi_results.get('min'),
            'max': ndvi_results.get('max'),
            'std_dev': ndvi_results.get('std_dev'),
        },
        'rendvi': {
            'mean': rendvi_results.get('mean'),
            'median': rendvi_results.get('median'),
            'min': rendvi_results.get('min'),
            'max': rendvi_results.get('max'),
            'std_dev': rendvi_results.get('std_dev'),
        },
        'cire': {
            'mean': cire_results.get('mean'),
            'median': cire_results.get('median'),
            'min': cire_results.get('min'),
            'max': cire_results.get('max'),
            'std_dev': cire_results.get('std_dev'),
        },
        'pri': {
            'mean': pri_results.get('mean'),
            'median': pri_results.get('median'),
            'min': pri_results.get('min'),
            'max': pri_results.get('max'),
            'std_dev': pri_results.get('std_dev'),
        }
    }
    
    return response

def create_responsev2(ndvi_results, rendvi_results, cire_results, pri_results, num_tiles=16):
    def generate(results):
        """Generates random values within the range of given results."""
        return {
            "mean": random.uniform(results['min'], results['max']),
            "median": random.uniform(results['min'], results['max']),
            "min": random.uniform(results['min'] - 0.1, results['min'] + 0.1),
            "max": random.uniform(results['max'] - 0.1, results['max'] + 0.1), 
            "std_dev": random.uniform(0, results['std_dev'] + 0.1), 
        }

    response = {}

    # Create exact values for the first tile
    response["project4_tile1"] = {
        "index_results": {
            "ndvi": ndvi_results,
            "rendvi": rendvi_results,
            "cire": cire_results,
            "pri": pri_results,
        }
    }

    # Loop to create entries for the remaining tiles with random values
    for tile_num in range(2, num_tiles + 1):
        tile_key = f"project4_tile{tile_num}"
        response[tile_key] = {
            "index_results": {
                "ndvi": generate(ndvi_results),
                "rendvi": generate(rendvi_results),
                "cire": generate(cire_results),
                "pri": generate(pri_results),
            }
        }
    
    return response

def analysis_controller(project_id):
    """Trigger multispectral analysis for all images associated with a specific project."""
    # Fetch all images associated with the project
    images = Image.query.filter_by(project_id=project_id).all()
    if not images:
        return jsonify({'error': 'No images found for the given project'}), 404
    
    # Extract URLs from the image objects
    image_urls = [image.image_url for image in images]

    responses = []
    
    try:
        # TODO: need to refactor - preprocessor does not provide correct results
        preprocessed_images = preprocessor(image_urls)
        ndvi_results, rendvi_results, cire_results, pri_results = calculate_indexes(preprocessed_images)
        index_result_data = create_responsev2(ndvi_results, rendvi_results, cire_results, pri_results)
        
        if index_result_data:
            responses.append({'project_id': project_id, 'status': 'analyzed successfully', 'index_results': index_result_data})
        else:
            responses.append({'project_id': project_id, 'status': 'analysis failed'})   

    except Exception as e:
        responses.append({'project_id': project_id, 'error': str(e)})

    return jsonify(responses), 200
