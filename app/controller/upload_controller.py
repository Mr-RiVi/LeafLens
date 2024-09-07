from flask import request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from app.service.image_upload_service import save_image
from app.model.project_model import Project

from app import db

def validate_project_id(project_id):
    # Check if the project ID exists in the database
    project = db.session.query(Project).filter_by(project_id=project_id).first()
    return project is not None

def image_upload_controller(project_id):
    # Validate project_id
    if not validate_project_id(project_id):
        return jsonify({'error': f'Project ID {project_id} does not exist'}), 404

    # Ensure the upload folder exists
    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.makedirs(current_app.config['UPLOAD_FOLDER'])

    # Check if any files are part of the request
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files[]')

    # If no files are provided
    if len(files) == 0:
        return jsonify({'error': 'No files selected for upload'}), 400

    responses = []

    # Process each file
    for file in files:
        if file.filename == '':
            responses.append({'error': 'No selected file'})
            continue

        # Save the file
        try:
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(save_path)

            # Save image metadata to the database
            image = save_image(filename=file.filename, project_id=project_id, image_url=save_path)
            responses.append({'filename': file.filename, 'status': 'uploaded successfully', 'image_id': image.image_id})
        except Exception as e:
            responses.append({'filename': file.filename, 'error': str(e)})

    return jsonify(responses), 200
