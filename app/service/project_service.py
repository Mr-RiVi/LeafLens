from app.model.project_model import Project
from app import db

def create_project(project_name, description):
    """Creates a new project and adds it to the database."""
    project = Project(project_name=project_name, description=description)
    db.session.add(project)
    db.session.commit()
    return project

# def create_task(project_id, task_id, task_status):
#     """Creates a new project and adds it to the database."""
#     project = Project(project_name=project_name, description=description)
#     db.session.add(project)
#     db.session.commit()
#     return project

def get_all_projects():
    """Fetches all project from the database."""
    return db.session.query(Project).all()