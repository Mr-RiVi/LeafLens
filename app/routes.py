from app import app
from app.controller.project_controller import create_project_controller, fetch_projects_controller
from app.controller.upload_controller import image_upload_controller
from app.controller.analysis_controller import analysis_controller, get_task_status

app.add_url_rule("/project/new", "create_project", create_project_controller, methods=['POST'])

app.add_url_rule("/project/list", "fetch_projects", fetch_projects_controller, methods=['GET'])

app.add_url_rule("/projects/<int:project_id>/upload", "image_upload", image_upload_controller, methods=['POST'])

app.add_url_rule("/project/<int:project_id>/start", "analyze_images", analysis_controller, methods=['POST'])

app.add_url_rule("/task-status/<task_id>", "task_status", get_task_status, methods=['GET'])

# curl --location --request POST 'http://127.0.0.1:5000/project/4/start'

# curl --location 'http://127.0.0.1:5000/projects/4/upload' \
# --form 'files[]=@"/home/fernando-mrr/Downloads/rgb_image/DJI_20240424101831_0001_D.jpg"' \
# --form 'files[]=@"/home/fernando-mrr/Downloads/rgb_image/DJI_20240424101831_0001_MS_G.TIF"' \
# --form 'files[]=@"/home/fernando-mrr/Downloads/rgb_image/DJI_20240424101831_0001_MS_NIR.TIF"' \
# --form 'files[]=@"/home/fernando-mrr/Downloads/rgb_image/DJI_20240424101831_0001_MS_R.TIF"' \
# --form 'files[]=@"/home/fernando-mrr/Downloads/rgb_image/DJI_20240424101831_0001_MS_RE.TIF"'