from flask import jsonify, current_app
import os

from app.service.image_preprocessor import preprocessor
from app.service.index_analysis_service import calculate_indexes

from app.model.image_model import Image

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
        # TODO: need to refactor - preprocessor dosent provide correct results
        preprocessed_images = preprocessor(image_urls) 
        result_data = calculate_indexes(preprocessed_images)
            
        if result_data:
            responses.append({'project Id': project_id, 'status': 'analyzed successfully'})
        else:
            responses.append({'project Id': project_id, 'status': 'analysis failed'})

    except Exception as e:
        responses.append({'project Id': project_id, 'error': str(e)})    

    return jsonify(responses), 200
