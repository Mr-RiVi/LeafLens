# from datetime import datetime, timezone

# from app import db

# class Task(db.Model):
#     __tablename__ = 'task'
#     project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
#     task_id = db.Column(db.String(255), primary_key=True)
#     task_status = db.Column(db.String(255), nullable=False)
#     task_results = db.Column(db.String(255), nullable=False)
#     created_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # project = db.relationship('Project', back_populates='task', lazy=True)