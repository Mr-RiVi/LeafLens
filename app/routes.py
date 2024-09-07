from app import app
from app.controller.project_controller import create_project_controller, fetch_projects_controller
from app.controller.upload_controller import image_upload_controller
from app.controller.analysis_controller import analysis_controller

app.add_url_rule("/project/new", "create_project", create_project_controller, methods=['POST'])

app.add_url_rule("/project/list", "fetch_projects", fetch_projects_controller, methods=['GET'])

app.add_url_rule("/projects/<int:project_id>/upload", "image_upload", image_upload_controller, methods=['POST'])

app.add_url_rule("/project/<int:project_id>/start", "analyze_images", analysis_controller, methods=['POST'])