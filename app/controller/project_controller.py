from flask import request, jsonify
from app.service.project_service import create_project, get_all_projects

def create_project_controller():
    data = request.json

    project_name = data.get('project_name')
    description = data.get('description')

    if not all([project_name, description]):
        return jsonify({"message": "Invalid input", "code": 400}), 400

    try:
        project = create_project(project_name, description)
        return jsonify({"message": "Project created successfully", "code": 200, "project_id": project.project_id}), 200
    except Exception as e:
        return jsonify({"message": str(e), "code": 500}), 500

def fetch_projects_controller():
    try:
        projects = get_all_projects()
        return jsonify({
            "data": [
                {
                    'project_id': project.project_id,
                    'project_name': project.project_name,
                    "description": project.description
                }
                for project in projects
            ],
            "message": "Projects fetched successfully", 
            "code": 200
        }), 200
    except Exception as e:
        return jsonify({"message": str(e), "code": 500}), 500
